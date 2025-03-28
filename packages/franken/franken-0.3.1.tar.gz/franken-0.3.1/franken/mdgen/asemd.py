import inspect
import logging
import os
import time
from pathlib import Path
from typing import Any, Union

import hydra
import hydra.core.global_hydra
import numpy as np
import torch
from omegaconf import DictConfig

import ase
import ase.calculators
import ase.calculators.calculator
import ase.io
import ase.io.trajectory
import ase.md.md
import ase.units
from franken.calculators.ase_calc import FrankenCalculator
from franken.backbones.utils import CacheDir, get_checkpoint_path, load_model_registry
from franken.mdgen.mdgen_utils import (
    FrankenMDLogger,
    MDError,
    get_md_nan_checker,
    register_hydra_resolvers,
)
from franken.utils.misc import pprint_config, remove_root_logger_handlers, setup_logger


try:
    from mace.calculators import MACECalculator  # type: ignore
except ImportError:
    MACECalculator = None
try:
    from fairchem.core.common.relaxation.ase_utils import OCPCalculator  # type: ignore
except ImportError:
    OCPCalculator = None

logger = logging.getLogger("franken")


def init_calculator(
    calc_type: str,
    model_path: Union[str, Path, None],
    device: Union[int, str, torch.device],
    **calc_kwargs,
) -> ase.calculators.calculator.Calculator:
    """Initialize the calculator based on the specified type from the given path.

    Args:
        calc_type
            Describes the calculator which should be used. Can be either 'franken',
            which loads a Franken model from the specified :code:`model_path`, one
            of the supported backbone families (e.g. "MACE", "fairchem") which use
            the calculators from the respective repositories, or it can also be a
            backbone ID (e.g. "MACE-L0") such that, if :code:`model_path` is not
            specified, the backbone itself is loaded as a model for MD simulations.
        model_path
            Optional path to the backbone used to compute energies and forces for
            the MD simulation.
        device
            Device on which the backbone should run.
        calc_kwargs
            Additional arguments to be passed to the Calculator class which corresponds
            to the chosen :code:`calc_type`. For the supported keyword arguments for
            the "franken" calculator, see :class:`franken.ase.FrankenCalculator`.
    Returns:
        Calculator
    """
    calc: ase.calculators.calculator.Calculator
    if calc_type == "franken":
        if model_path is None:
            raise ValueError(
                f"Model path must not be 'None' for calculator of type '{calc_type}'. "
                "Check your config file and re-run asemd."
            )
        calc = FrankenCalculator(model_path, device=device, **calc_kwargs)
    else:
        registry = load_model_registry()
        backbone_families = set([entry["kind"] for entry in registry.values()])
        if calc_type in backbone_families:
            if model_path is None:
                raise ValueError(
                    f"Model path must not be 'None' for calculator of type '{calc_type}'. "
                    "Check your config file and re-run asemd."
                )
            calc_family = calc_type
        elif calc_type in registry:
            calc_family = registry[calc_type]["kind"]
            if model_path is None:
                logger.info(
                    f"Model path was not specified for calculator of type '{calc_type}'. "
                    f"Using the default model downloaded from '{registry[calc_type]['remote']}'"
                )
                model_path = get_checkpoint_path(calc_type)
        else:
            raise ValueError(
                f"Calculator of type '{calc_type}' is not valid. "
                f"Expected 'franken', a backbone family "
                f"(i.e. one of {backbone_families}) or a valid model ID."
            )
        # Initialize the Fairchem/Mace calculators
        if calc_family == "MACE":
            if MACECalculator is None:
                raise ImportError(
                    f"Failed to initialize calculator of type '{calc_type}' "
                    "because mace could not be imported. Check that mace is "
                    "installed in the current environment."
                )
            calc = MACECalculator(str(model_path), device=str(device), **calc_kwargs)
            # MACE Adds a root-level logger which makes all logs print out duplicates
            remove_root_logger_handlers()
        elif calc_family == "fairchem":
            if OCPCalculator is None:
                raise ImportError(
                    f"Failed to initialize calculator of type '{calc_type}' "
                    "because fairchem could not be imported. Check that fairchem is "
                    "installed in the current environment."
                )
            calc = OCPCalculator(
                checkpoint_path=str(model_path),
                cpu=torch.device(device).type != "cuda",
                **calc_kwargs,
            )
            calc.trainer.model.float()  # type: ignore
        else:
            raise NotImplementedError(
                f"Calculator for backbone family '{calc_family}' is not implemented."
                " Only 'MACE' and 'fairchem' families have an implemented calculator."
            )
    return calc


def cfg_fn_has_param(cfg, param_name):
    import hydra._internal.instantiate._instantiate2

    init_v_func = hydra._internal.instantiate._instantiate2._resolve_target(
        cfg._target_, ""
    )
    return param_name in inspect.signature(init_v_func).parameters.keys()


def run_md_simulation(
    output_dir: Path,
    integrator_cfg,
    initial_velocity_cfg,
    initial_configuration: ase.Atoms,
    num_steps: int,
    save_every: int,
    log_every: int,
    seed: int,
    output_format="traj",
):
    """Run MD simulation for given atoms at a specific temperature."""
    if num_steps == 0:
        return output_dir / f"replica_{seed}.{output_format}"

    # Set random seed
    torch.manual_seed(seed)
    np.random.seed(seed)

    # Initialize velocities/conditions if given.
    ## assert (initial_configuration.get_momenta() == 0).all()
    # Extra parameters to velocity initialization always include the
    # initial configuration. Sometimes also a specific rng (not all
    # velocity inits are random!)
    extra_params: dict[str, Any] = {"atoms": initial_configuration}
    if initial_velocity_cfg is not None:
        if cfg_fn_has_param(initial_velocity_cfg, "rng"):
            extra_params["rng"] = np.random.default_rng(seed=seed)
            hydra.utils.call(initial_velocity_cfg, **extra_params)

    # Initialize trajectory
    trajectory_path = output_dir / f"replica_{seed}.traj"
    if trajectory_path.exists():
        logger.warning(
            f"Trajectory path '{trajectory_path.resolve()}' already exists and will be overwritten."
        )
    trajectory = ase.io.Trajectory(trajectory_path, "w", initial_configuration)
    assert isinstance(trajectory, ase.io.trajectory.TrajectoryWriter)

    # MD Setup and running
    logger.info(f"{num_steps} steps of MD simulation starting...")
    t_start = time.time()
    integrator = hydra.utils.instantiate(
        integrator_cfg,
        atoms=initial_configuration,
    )
    md_logger = FrankenMDLogger(
        dynamics=integrator,
        atoms=initial_configuration,
        stress=False,
        peratom=False,
    )
    # nan checker needs to go first to be effective.
    integrator.attach(get_md_nan_checker(atoms=initial_configuration), interval=1)
    integrator.attach(trajectory.write, interval=save_every)
    integrator.attach(md_logger, interval=log_every)
    try:
        integrator.run(num_steps)
        t_end = time.time()
        logger.info(f"{num_steps} simulation steps complete in {t_end - t_start:.2f}s.")
    except MDError as e:
        t_end = time.time()
        logger.error(f"Simulation failed after {t_end - t_start:.2f}s.", exc_info=e)

    if output_format != "traj":
        logger.info(f"Converting ASE traj to the specified format {output_format}")
        traj = ase.io.read(trajectory_path, index=":")
        new_trajectory_path = output_dir / f"replica_{seed}.{output_format}"
        if new_trajectory_path.exists():
            logger.warning(
                f"Trajectory path '{new_trajectory_path.resolve()}' already exists and will be overwritten."
            )
        ase.io.write(new_trajectory_path, traj)
        os.remove(trajectory_path)
        return new_trajectory_path
    return trajectory_path


def md_main(cfg: DictConfig):
    output_dir = Path(cfg.paths.run_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if torch.cuda.is_available():
        device = torch.device(torch.cuda.current_device())
    else:
        device = torch.device("cpu")

    logging_level = cfg.console_logging_level.upper()
    setup_logger(level=logging_level, directory=output_dir, logname="asemd")
    pprint_config(cfg)

    CacheDir.initialize()

    # Load initial configuration
    init_config_index = cfg.get("init_config_index", 0)
    init_config = ase.io.read(str(cfg.init_config_path), index=init_config_index)
    assert isinstance(init_config, ase.Atoms)  # check we didn't read list[Atoms]

    # if the system has hydrogen atoms, set their mass according to config (default=1 a.u.)
    if (init_config.get_atomic_numbers() == 1).any() and "hydrogen_mass" in cfg:
        mass_H = cfg.get("hydrogen_mass")
        masses = init_config.get_masses()
        init_config.get_masses()[init_config.get_atomic_numbers() == 1] = mass_H
        init_config.set_masses(masses)

        logger.info(f"Setting hydrogen mass to {int(mass_H)} a.u.")

    # Initialize calculator
    calc = init_calculator(**cfg.calculator, device=device)

    # Setup a few MD parameters
    num_md_steps = int(round(cfg.md_length_ns * 1e6 / cfg.timestep_fs))

    # Get seeds from configs
    seeds = [cfg.seed] if isinstance(cfg.seed, int) else cfg.seed

    # Run MD
    traj_paths = []
    for i, seed in enumerate(seeds):
        rep_init = init_config.copy()
        rep_init.calc = calc
        saved_path = run_md_simulation(
            output_dir=output_dir,
            integrator_cfg=cfg.integrator,
            initial_velocity_cfg=cfg.initial_velocity,
            initial_configuration=rep_init,
            num_steps=num_md_steps,
            output_format=cfg.output_format,
            save_every=cfg.save_every,
            log_every=cfg.log_every,
            seed=seed,
        )
        traj_paths.append(saved_path)
        logger.info(f"Replica {i} ({seed=}, {cfg.temperature_K=:.1f}K) finished")
        logger.info(f"Run output can be found at '{saved_path.resolve()}'")
        print()  # just for nicer output


@hydra.main(version_base="1.3", config_path="configs", config_name="md_run.yaml")
def hydra_entry_point(cfg: DictConfig):
    md_main(cfg)


def md_cli_entry_point():
    register_hydra_resolvers()
    hydra_entry_point()


def asemd(*overrides: str):
    # Entry point for scripts
    hydra.initialize(version_base="1.3", config_path="configs")
    try:
        cfg = hydra.compose("md_run.yaml", overrides=list(overrides))
        md_main(cfg)
    finally:
        hydra.core.global_hydra.GlobalHydra.instance().clear()


if __name__ == "__main__":
    md_cli_entry_point()
