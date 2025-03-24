import hashlib
import logging
from pathlib import Path

import hydra
from omegaconf import DictConfig
import torch

from franken.autotune.script import init_loaders
from franken.backbones.utils import CacheDir
from franken.rf.model import FrankenPotential
from franken.trainers.log_utils import LogCollection
from franken.trainers.rf_cuda_lowmem import RandomFeaturesTrainer
import franken.utils.distributed as dist_utils
from franken.utils.misc import pprint_config, setup_logger


logger = logging.getLogger("franken")


@hydra.main(version_base="1.3", config_path="configs", config_name="evaluate.yaml")
def _evaluate(cfg: DictConfig):
    """
    Load a model and evaluate it on a given dataset
    """
    # Load all needed configuration keys immediately
    logging_level = cfg.get("console_logging_level", "WARNING").upper()
    data_path = Path(cfg.data_path)
    model_path = Path(cfg.model_path)
    model_info_path = (
        Path(cfg.model_info_path) if cfg.get("model_info_path") is not None else None
    )
    rf_weight_id = cfg.get("rf_weight_id", 0)
    log_out_path = Path(cfg.save_path)
    run_dir = Path(cfg.run_dir) if cfg.get("run_dir") is not None else None
    if run_dir is None:
        run_dir = model_path if model_path.is_dir() else model_path.parent

    if torch.cuda.is_available():
        rank = dist_utils.init()
        device = torch.device(torch.cuda.current_device())
    else:
        rank = 0
        device = torch.device("cpu")
    # Create run folder (from a single rank)
    if rank != 0:
        run_dir = None
        dist_utils.barrier()
    else:
        run_dir.mkdir(parents=True, exist_ok=True)
        dist_utils.barrier()  # other ranks follow

    setup_logger(
        level=logging_level,
        directory=dist_utils.broadcast_obj(run_dir),
        rank=rank,
        logname="franken_eval",
    )
    pprint_config(cfg)

    if log_out_path.is_dir():
        raise ValueError(
            f"'save_path' '{log_out_path.resolve()}' is a directory. It must be a file."
        )
    if not log_out_path.name.endswith(".json"):
        log_out_path = Path(str(log_out_path.resolve()) + ".json")
    if log_out_path.exists():
        logger.warning(
            f"'save_path' '{log_out_path.resolve()}' already exists and will be overwritten."
        )

    CacheDir.initialize()

    # Figure out the path to the model
    if model_path.is_dir():
        _model_path = model_path / "best_ckpt.pt"
        if not _model_path.exists():
            raise FileNotFoundError(
                f"Inferred model path '{_model_path.resolve()}' does not exist."
            )
    else:
        _model_path = model_path
        if not _model_path.exists():
            raise FileNotFoundError(
                f"Model path '{_model_path.resolve()}' does not exist."
            )

    # Load model. Splitting the ranks here since initializing FrankenPotential
    # can result in backbone download. We avoid double download.
    if rank != 0:
        dist_utils.barrier()
    logger.info(f"Loading FrankenPotential from '{_model_path.resolve()}'")
    franken = FrankenPotential.load(
        _model_path,
        map_location=device,
        rf_weight_id=rf_weight_id,
    )
    model_hash = hashlib.md5(str(franken.hyperparameters).encode())
    model_hash = model_hash.hexdigest()
    if rank == 0:
        dist_utils.barrier()

    data_loader = init_loaders(
        franken.gnn_backbone_id,
        train_path=None,
        test_path=data_path,
    )["test"]

    # Figure out path to the model info (LogEntry corresponding to the model)
    if model_info_path is None:
        if model_path.is_dir() and (model_path / "best.json").exists():
            model_info_path = model_path / "best.json"
    elif model_info_path.is_dir():
        model_info_path = model_info_path / "log.json"
    if model_info_path is None:
        raise FileNotFoundError(
            "Could not infer model_info_path. Pass it to the program explicitly."
        )
    if not model_info_path.exists():
        raise FileNotFoundError(
            f"Could not find explicit model_info_path at '{model_info_path.resolve()}'"
        )

    # Load logs and check correspondence to model
    logger.info(f"Loading LogCollection from '{model_info_path.resolve()}'")
    log_collection = LogCollection.from_json(model_info_path)
    model_info = None
    for log_entry in log_collection:
        if log_entry.checkpoint_hash == model_hash:
            model_info = log_entry
            break
    if model_info is None and len(log_collection) == 1:
        logger.warning("Model hash does not correspond with log hash")
        model_info = log_collection[0]
    elif model_info is None:
        raise ValueError(
            f"Could not find model-info at '{model_info_path.resolve()}' corresponding to loaded franken model"
        )

    trainer = RandomFeaturesTrainer(
        train_dataloader=None,  # type: ignore
        log_dir=None,
        device=device,
    )
    eval_logs = trainer.evaluate(
        model=franken,
        dataloader=data_loader,
        log_collection=LogCollection([model_info]),
        all_weights=None,
    )
    if rank == 0:
        eval_logs.save_json(log_out_path)
        logger.info(f"Saved evaluation logs to {log_out_path}")


def evaluate():
    _evaluate()


if __name__ == "__main__":
    evaluate()
