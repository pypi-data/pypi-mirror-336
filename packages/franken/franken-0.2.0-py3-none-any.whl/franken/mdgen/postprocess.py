from typing import Literal, Sequence
import itertools
import json
import logging

from ase import Atoms
from ase.geometry.rdf import get_recommended_r_max
from ase.io import read
import ase.data
import hydra
import numpy as np
from pathlib import Path
from omegaconf import DictConfig

from franken.backbones.utils import CacheDir
from franken.mdgen.diffusion_coeff import calc_self_diffusion, calc_water_msd
from franken.mdgen.mdgen_utils import register_hydra_resolvers
from franken.utils.misc import pprint_config, setup_logger
from franken.mdgen.rdf_utils import (
    distance_matrix,
    avg_rdf,
    compute_rdf_mae,
    stability_rdf,
)

logger = logging.getLogger("franken")


class NumpyEncoder(json.JSONEncoder):
    """JSON encoder to dump numpy arrays as python lists"""

    def default(self, o):
        if isinstance(o, np.ndarray):
            return o.tolist()
        return super().default(o)


def read_traj(path) -> list[Atoms]:
    traj = read(path, index=":")
    if isinstance(traj, Atoms):
        traj = [traj]
    return traj


def get_rmax(*trajs: list[Atoms]) -> float:
    rmax = float("inf")
    for traj in trajs:
        for frame in traj:
            rmax = min(rmax, get_recommended_r_max(frame.cell, frame.pbc))  # type: ignore
    return rmax


def postprocessing_water_diffusion_coef(
    traj_paths: list[Path], timestep_fs: float, t_min_fs: float = 0.0
) -> dict[str, dict]:
    # Loop over trajectories
    results = {}
    for traj_path in traj_paths:
        name = traj_path.stem
        if not traj_path.exists():
            logger.warning(f"Trajectory {name} does not exist. Skipping.")
            continue
        logger.info(f"Water diffusion coefficient for trajectory {name}...")
        results[name] = {}

        traj = read_traj(traj_path)

        msd = calc_water_msd(traj)
        ds, linmods = calc_self_diffusion(
            msd, delta_t_fs=timestep_fs, t_min=None, t_min_fs=t_min_fs
        )
        # Report all possibly useful data in a serializable way
        results[name]["MSD"] = msd
        results[name]["D"] = ds
        results[name]["slope"] = [lm.slope for lm in linmods]  # type: ignore
        results[name]["intercept"] = [lm.intercept for lm in linmods]  # type: ignore
        results[name]["stderr"] = [lm.stderr for lm in linmods]  # type: ignore
        results[name]["intercept_stderr"] = [lm.intercept_stderr for lm in linmods]  # type: ignore
    return results


def postprocessing_rdf(
    traj_paths: list[Path],
    ref_traj_path: Path | None,
    timestep_fs: float,
    nbins_per_angstrom=50,
    stability_threshold=1.0,
    stability_interval: int = 20,
    equilibration_fs: float = 200,
    rdf_version: Literal["fast", "ase"] = "fast",
    distance_version: Literal["fast", "ase"] = "fast",
) -> dict[str, dict]:
    # Load reference
    ref_traj, ref_distance_matrix = None, None
    if ref_traj_path is not None:
        ref_traj = read_traj(ref_traj_path)
        ref_distance_matrix = distance_matrix(ref_traj, version=distance_version)

    # Loop over trajectories
    results = {}
    for traj_path in traj_paths:
        name = traj_path.stem
        if not traj_path.exists():
            logger.warning(f"Trajectory {name} does not exist. Skipping.")
            continue
        logger.info(f"RDF analysis for trajectory {name}...")
        results[name] = {}

        # Load traj and compute distances
        traj = read_traj(traj_path)
        # Skip first time-step which is just the initial configuration
        traj = traj[1:]
        # Skip the beginning of the trajectory where simulation is not at equilibrium
        traj_len_fs = timestep_fs * len(traj)
        if traj_len_fs <= equilibration_fs:
            # Did not reach equilibrium time
            results[name]["total_traj_time"] = 0
            results[name]["total_traj_time_fs"] = 0
            continue
        else:
            traj = traj[int(equilibration_fs / timestep_fs) :]
        results[name]["total_traj_time"] = len(traj)
        results[name]["total_traj_time_fs"] = len(traj) * timestep_fs
        traj_distance_matrix = distance_matrix(traj, version=distance_version)

        # Rmax and nbins for this trajectory
        if ref_traj is not None:
            rmax = get_rmax(ref_traj, traj)
        else:
            rmax = get_rmax(traj)
        nbins = int(rmax * nbins_per_angstrom)

        unique_atomic_numbers = np.unique(traj[0].numbers)
        # Since the inter-atomic distance is symmetric we don't care about ordering i.e. (1, 8), (8, 1)
        # therefore don't use carthesian product, get all length 2 combinations using this other
        # itertools function
        element_pairs = list(
            itertools.combinations_with_replacement(unique_atomic_numbers, 2)
        )
        for el_pair in element_pairs:
            el_pair = tuple(sorted(el_pair))  # for consistency
            el_pair_str = f"{ase.data.chemical_symbols[el_pair[0]]}-{ase.data.chemical_symbols[el_pair[1]]}"
            # Full RDF for test trajectory
            full_traj_rdf, radii = avg_rdf(
                traj,
                distance_matrix=traj_distance_matrix,
                rmax=rmax,
                nbins=nbins,
                elements=el_pair,
                version=rdf_version,
            )
            results[name][f"{el_pair_str}_rdf"] = full_traj_rdf
            # radii won't change with different elements.
            results[name]["dists"] = radii
            # Stability of the trajectory with respect to the average of the trajectory itself
            stability_time_self, stability_mae_self = stability_rdf(
                traj=traj,
                dist=traj_distance_matrix,
                ref_rdf=full_traj_rdf,
                rmax=rmax,
                nbins=nbins,
                stability_interval=stability_interval,
                threshold=stability_threshold,
                elements=el_pair,
                rdf_version=rdf_version,
            )
            results[name][f"{el_pair_str}_stability_time_self"] = stability_time_self
            results[name][f"{el_pair_str}_stability_mae_self"] = stability_mae_self

            # Stability of the trajectory with respect to the reference trajectory
            if ref_traj is not None:
                assert ref_distance_matrix is not None
                # Compute reference RDF. Recompute needed since rmax may have changed
                ref_rdf = avg_rdf(
                    ref_traj,
                    distance_matrix=ref_distance_matrix,
                    rmax=rmax,
                    nbins=nbins,
                    no_dists=True,
                    elements=el_pair,
                    version=rdf_version,
                )
                assert isinstance(ref_rdf, np.ndarray)
                results[name][f"{el_pair_str}_ref_rdf"] = ref_rdf
                full_mae = compute_rdf_mae(
                    full_traj_rdf, ref_rdf, delta_r=radii[1] - radii[0]
                )
                results[name][f"{el_pair_str}_rdf_mae"] = full_mae
                stability_time_ref, stability_mae_ref = stability_rdf(
                    traj=traj,
                    dist=traj_distance_matrix,
                    ref_rdf=ref_rdf,
                    rmax=rmax,
                    nbins=nbins,
                    stability_interval=stability_interval,
                    threshold=stability_threshold,
                    elements=el_pair,
                    rdf_version=rdf_version,
                )
                results[name][f"{el_pair_str}_stability_time_ref"] = stability_time_ref
                results[name][f"{el_pair_str}_stability_mae_ref"] = stability_mae_ref
    return results


def save_analysis_results(
    traj_paths: list[Path], results: Sequence[dict], save_full: bool = True
) -> None:
    # Check that the results are consistent (all analyses have same 'trajectory-name' keys)
    valid_names = set(results[0].keys())
    for anl_res in results:
        if set(anl_res.keys()) != valid_names:
            logger.error(
                f"Cannot save postprocessing results. Trajectory names differ between analyses. "
                f"Valid file-names are {valid_names}, found names {set(anl_res.keys())}."
            )
            return

    # Save the analyses for individual trajectories
    save_folder = None
    merged_analysis = {}
    for traj_path in traj_paths:
        name = traj_path.stem

        save_folder = traj_path.parent
        save_path = save_folder / f"{name}_analysis.json"
        with open(save_path, "w") as f:
            merged_traj_analysis = {
                k: v for anl_res in results for k, v in anl_res[name].items()
            }
            merged_analysis[name] = merged_traj_analysis
            json.dump(merged_traj_analysis, f, cls=NumpyEncoder)
        logger.info(f"Saved postprocessing results to: '{save_path.resolve()}'")

    # save the whole analysis as well.
    if save_full and save_folder is not None:
        if not all(traj_paths[0].parent == tp.parent for tp in traj_paths):
            logger.warning(
                "Cannot save full analysis because trajectories are not in the same folder."
            )
        else:
            save_path = traj_paths[0].parent / "analysis.json"
            if save_path.exists():
                logger.warning(
                    f"Full analysis save-path '{save_path.resolve()}' exists and will be overwritten."
                )
            with open(save_path, "w") as f:
                json.dump(merged_analysis, f, cls=NumpyEncoder)
            logger.info(
                f"Saved whole postprocessing results to: '{save_path.resolve()}'"
            )


@hydra.main(
    version_base="1.3", config_path="configs", config_name="md_postprocess.yaml"
)
def md_postprocess(cfg: DictConfig):
    output_dir = Path(cfg.paths.run_dir)
    logging_level = cfg.console_logging_level.upper()
    setup_logger(level=logging_level, directory=output_dir, logname="asemd")
    pprint_config(cfg)
    if not CacheDir.is_initialized():
        CacheDir.initialize()

    # Find traj paths
    traj_ext = "extxyz"
    trajectories = list(output_dir.glob(f"*.{traj_ext}"))
    if len(trajectories) == 0:
        raise RuntimeError(
            f"No trajectory with extension {traj_ext} found "
            f"in output directory {output_dir}"
        )
    logger.info(f"Found {len(trajectories)} to postprocess")

    all_analyses = []
    post_configs = cfg.metrics
    for post_name, post_cfg in post_configs.items():
        logger.info(f"Running {post_name} postprocessing...")
        all_analyses.append(hydra.utils.instantiate(post_cfg, traj_paths=trajectories))
    if len(all_analyses) > 0:
        save_analysis_results(traj_paths=trajectories, results=all_analyses)

    logger.info("Postprocessing complete.")


def pp_cli_entry_point():
    register_hydra_resolvers()
    md_postprocess()


if __name__ == "__main__":
    pp_cli_entry_point()
