import datetime
import json
import logging
import warnings
from pathlib import Path
from typing import Any, Dict, Literal, NamedTuple, Optional, Tuple
from uuid import uuid4

import hydra
import hydra.core.global_hydra
import torch.distributed
import torch.utils.data
from omegaconf import DictConfig, OmegaConf

from franken.datasets.registry import DATASET_REGISTRY
import franken.utils.distributed as dist_utils
from franken.backbones.utils import CacheDir, download_checkpoint
from franken.data import BaseAtomsDataset
from franken.rf.model import FrankenPotential
from franken.trainers import BaseTrainer
from franken.trainers.log_utils import DataSplit, LogEntry
from franken.utils.misc import (
    garbage_collection_cuda,
    get_device_name,
    params_grid,
    pprint_config,
    setup_logger,
)


class BestTrial(NamedTuple):
    trial_id: int
    log: LogEntry


warnings.filterwarnings(
    "ignore",
    message=r"You are using `torch.load` with `weights_only=False`",
    category=FutureWarning,
)
warnings.filterwarnings(
    "ignore",
    message=r"`torch.cuda.amp.autocast\(args...\)` is deprecated",
    category=FutureWarning,
)
logger = logging.getLogger("franken")


def init_loaders(
    gnn_backbone_id: str,
    train_path: Optional[Path],
    val_path: Optional[Path] = None,
    test_path: Optional[Path] = None,
    num_train_subsamples: int | None = None,
    subsample_rng: int | None = None,
) -> Dict[str, torch.utils.data.DataLoader]:
    datasets: Dict[str, BaseAtomsDataset] = {}
    for split, data_path in zip(
        ["train", "val", "test"], [train_path, val_path, test_path]
    ):
        if data_path is not None:
            dset = BaseAtomsDataset.from_path(
                data_path=data_path,
                split=split,
                gnn_backbone_id=gnn_backbone_id,
                num_random_subsamples=(
                    num_train_subsamples if split == "train" else None
                ),
                subsample_rng=subsample_rng,
            )
            datasets[split] = dset

    dataloaders = {
        split: dset.get_dataloader(distributed=torch.distributed.is_initialized())
        for split, dset in datasets.items()
    }
    return dataloaders


def create_params_grid(
    group_name: Literal["random_features", "solver"],
    group: DictConfig,
):
    group_dict = {}

    for k, v in group.items():
        if k == "num_random_features":
            assert isinstance(
                v, int
            ), f"The number of random features should not be optimized over. Got num_random_features={v} {type(v)}"

        if isinstance(v, DictConfig) and "_target_" in v:
            v = hydra.utils.instantiate(v)
        elif isinstance(v, (int, float)):
            v = [v]

        group_dict[k] = v

    if group_name == "solver":
        return group_dict
    else:
        return params_grid(group_dict)


def filter_rf_hp_grid(rf_hp: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    # if num_species is None, chemically_informed_ratio must also be None
    if rf_hp.get("num_species", None) is None:
        if rf_hp.get("chemically_informed_ratio", None) is not None:
            return None
    return rf_hp


def hp_summary_str(trial_id: int, current_best: BestTrial, parameters: dict) -> str:
    hp_summary = f"Trial {trial_id + 1:>3} |"
    for k, v in parameters.items():
        fmt_val = format(v, ".3f" if isinstance(v, float) else "")
        hp_summary += f" {k:^7}: {fmt_val:^7} |"
    try:
        energy_error = current_best.log.get_metric("energy_MAE", DataSplit.VALIDATION)
        forces_error = current_best.log.get_metric("forces_MAE", DataSplit.VALIDATION)
    except KeyError:
        energy_error = current_best.log.get_metric("energy_MAE", DataSplit.TRAIN)
        forces_error = current_best.log.get_metric("forces_MAE", DataSplit.TRAIN)

    hp_summary += (
        f" Best trial {current_best.trial_id} (energy {energy_error:.2f} meV/atom - "
        f"forces {forces_error:.1f} meV/Ang)"
    )
    return hp_summary


def run_autotune(
    rnd_seed: int,
    gnn_backbone_id: str,
    interaction_block: int,
    rf_type: str,
    loaders: Dict[str, torch.utils.data.DataLoader],
    rf_param_grid,
    solver_param_grid,
    scale_by_Z: bool,
    atomic_energies: Dict[int, torch.Tensor],
    jac_chunk_size: int | Literal["auto"],
    trainer: BaseTrainer,
):
    current_best = BestTrial(None, None)
    for trial_id, parameters_instance in rf_param_grid:
        logger.debug(f"Autotune iteration with RF parameters {parameters_instance}")
        if rf_type in ["poly", "gaussian", "biased-gaussian", "multiscale-gaussian"]:
            random_features_params = {"rng_seed": rnd_seed} | parameters_instance
        elif rf_type == "linear":
            random_features_params = parameters_instance
        else:
            raise ValueError(rf_type)

        model = FrankenPotential(
            gnn_backbone_id,
            rf_type,
            random_features_params,
            interaction_block=interaction_block,
            scale_by_Z=scale_by_Z,  # TODO: This should be a param we can do hp-search on
            num_species=loaders["train"].dataset.num_species,
            atomic_energies=atomic_energies,
            jac_chunk_size=jac_chunk_size,
        )

        logs, weights = trainer.fit(model, solver_param_grid)
        for split_name, loader in loaders.items():
            logs = trainer.evaluate(model, loader, logs, weights)
        split_for_best_model = (
            DataSplit.VALIDATION if "val" in loaders else DataSplit.TRAIN
        )
        if dist_utils.get_rank() == 0:
            if trainer.log_dir is not None:
                trainer.serialize_logs(model, logs, weights, split_for_best_model)
        dist_utils.barrier()

        # current best model update
        if dist_utils.get_rank() == 0:
            if trainer.log_dir is not None:
                with open(trainer.log_dir / "best.json", "r") as f:
                    try:
                        best_log = LogEntry.from_dict(json.load(f))
                        if best_log != current_best.log:
                            current_best = BestTrial(
                                trial_id=trial_id + 1,
                                log=best_log,
                            )
                    except KeyError:
                        pass

                logger.info(hp_summary_str(trial_id, current_best, parameters_instance))
        garbage_collection_cuda()


def create_run_folder(base_run_dir: Path) -> Path:
    # Use time + a shortened UUID to ensure uniqueness of
    # the experiment directory. The names will look like
    # 'run_240926_113513_1d93b3ed'
    now_str = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    exp_dir_name = f"run_{now_str}_{uuid4().hex[:8]}"
    exp_dir = base_run_dir / exp_dir_name
    exp_dir.mkdir(parents=True, exist_ok=True)
    return exp_dir


def save_experiment_info(cfg: DictConfig, run_dir: Path):
    train_hardware = {
        "num_gpus": dist_utils.get_world_size(),
        "gpu_model": get_device_name("cuda:0"),
        "cpu_model": get_device_name("cpu"),
    }
    cfg_dict = OmegaConf.to_container(cfg, resolve=True)
    assert isinstance(cfg_dict, dict)
    with open(run_dir / "configs.json", "w") as f:
        json.dump(cfg_dict | train_hardware, f, indent=4)


def get_dataset_paths(
    train_path: Optional[str],
    val_path: Optional[str],
    test_path: Optional[str],
    dataset_name: Optional[str],
) -> Tuple[Path, Optional[Path], Optional[Path]]:
    try:
        if dataset_name is None:
            raise KeyError
        out_train_path = DATASET_REGISTRY.get_path(
            dataset_name, "train", CacheDir.get()
        )
        out_val_path = None
        if DATASET_REGISTRY.is_valid_split(dataset_name, "val"):
            out_val_path = DATASET_REGISTRY.get_path(
                dataset_name, "val", CacheDir.get()
            )
        out_test_path = None
        if DATASET_REGISTRY.is_valid_split(dataset_name, "test"):
            out_test_path = DATASET_REGISTRY.get_path(
                dataset_name, "test", CacheDir.get()
            )
    except KeyError as e:
        print(e)
        logger.info(f"Dataset with name '{dataset_name}' not found in registry")
        if train_path is None:
            raise ValueError(
                "Either a valid 'dataset_name' or 'train_path' must be "
                "specified in order to load a training dataset."
            )
        out_train_path = Path(train_path)
        out_val_path = Path(val_path) if val_path is not None else None
        out_test_path = Path(test_path) if test_path is not None else None
    return out_train_path, out_val_path, out_test_path


def main(cfg: DictConfig):
    run_dir = Path(cfg.paths.run_dir)

    if torch.cuda.is_available():
        rank = dist_utils.init(distributed=cfg.distributed)
        device = torch.device(torch.cuda.current_device())
    else:
        rank = 0
        device = torch.device("cpu")

    if rank != 0:  # first rank goes forward
        run_dir = None
        dist_utils.barrier()
    else:
        run_dir = create_run_folder(run_dir)
        dist_utils.barrier()  # other ranks follow
    logging_level = cfg.get("console_logging_level", "WARNING").upper()
    setup_logger(
        level=logging_level, directory=dist_utils.broadcast_obj(run_dir), rank=rank
    )
    pprint_config(cfg)

    # Global try-catch after setup_logger, to log any exceptions.
    try:
        CacheDir.initialize()

        if rank != 0:  # first rank goes forward
            dist_utils.barrier()
        else:
            save_experiment_info(cfg, run_dir)
            # Download the checkpoint if not present locally
            download_checkpoint(cfg.franken.gnn_backbone_id)
            logger.info(f"Run folder: {run_dir}")
            dist_utils.barrier()

        train_path, val_path, test_path = get_dataset_paths(
            cfg.dataset.get("train_path", None),
            cfg.dataset.get("val_path", None),
            cfg.dataset.get("test_path", None),
            cfg.dataset.get("dataset_name", None),
        )

        loaders = init_loaders(
            cfg.franken.gnn_backbone_id,
            train_path,
            val_path,
            test_path,
            cfg.dataset.train_subsample.num,
            cfg.dataset.train_subsample.rng_seed,
        )

        # Create HP sweep with "random_features" and "solver" groups.
        sweep = {}
        for group_name, group in cfg.hyperparameters.items():
            sweep[group_name] = create_params_grid(group_name, group)

        trainer: BaseTrainer = hydra.utils.instantiate(
            cfg.trainer,
            train_dataloader=loaders["train"],
            log_dir=run_dir,
            device=device,
        )

        if device.type == "cuda":
            from franken.backbones.wrappers.common_patches import patch_e3nn

            patch_e3nn()

        run_autotune(
            rnd_seed=cfg.seed,
            gnn_backbone_id=cfg.franken.gnn_backbone_id,
            interaction_block=cfg.franken.interaction_block,
            rf_type=cfg.franken.kernel_type,
            loaders=loaders,
            rf_param_grid=sweep["random_features"],
            solver_param_grid=sweep["solver"],
            scale_by_Z=cfg.franken.scale_by_Z,
            atomic_energies=cfg.franken.atomic_energies,
            jac_chunk_size=cfg.franken.jac_chunk_size,
            trainer=trainer,
        )
    except Exception as e:
        logger.error("Error encountered in autotune. Exiting.", exc_info=e)
        raise
    finally:
        if torch.distributed.is_initialized():
            torch.distributed.destroy_process_group()

    return run_dir


@hydra.main(version_base="1.3", config_path="configs", config_name="master.yaml")
def cli_entry_point(cfg: DictConfig):
    main(cfg)


def autotune(*overrides: str):
    # Entry point for scripts
    hydra.initialize(version_base="1.3", config_path="configs")
    try:
        cfg = hydra.compose("master.yaml", overrides=list(overrides))
        main(cfg)
    finally:
        hydra.core.global_hydra.GlobalHydra.instance().clear()


if __name__ == "__main__":
    cli_entry_point()
