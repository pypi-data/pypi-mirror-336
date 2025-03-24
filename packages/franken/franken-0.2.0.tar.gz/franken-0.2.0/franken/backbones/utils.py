import importlib.resources
import json
import logging
import os
from pathlib import Path

import requests
import torch
import torch.utils.data
from tqdm import tqdm


logger = logging.getLogger("franken")


def load_model_registry():
    model_registry_text = (
        importlib.resources.files("franken.backbones")
        .joinpath("registry.json")
        .read_text()
    )
    model_registry = json.loads(model_registry_text)
    return model_registry


class CacheDir:
    directory: Path | None = None

    @staticmethod
    def initialize(cache_dir: Path | str | None = None):
        if CacheDir.is_initialized():
            logger.warning(
                f"Cache directory already initialized at {CacheDir.directory}. Reinitializing."
            )
        # Default cache location: ~/.franken
        default_cache = Path.home() / ".franken"
        if cache_dir is None:
            env_cache_dir = os.environ.get("FRANKEN_CACHE_DIR", None)
            if env_cache_dir is None:
                logger.info(f"Initializing default cache directory at {default_cache}")
                cache_dir = default_cache
            else:
                logger.info(
                    f"Initializing cache directory from $FRANKEN_CACHE_DIR {env_cache_dir}"
                )
                cache_dir = env_cache_dir
        else:
            logger.info(f"Initializing custom cache directory {cache_dir}")
        CacheDir.directory = Path(cache_dir)

        # Ensure the directory exists
        if not CacheDir.directory.exists():
            CacheDir.directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created cache directory at: {CacheDir.directory}")

    @staticmethod
    def get() -> Path:
        if not CacheDir.is_initialized():
            CacheDir.initialize()
        assert CacheDir.directory is not None
        return CacheDir.directory

    @staticmethod
    def is_initialized() -> bool:
        return CacheDir.directory is not None


def make_summary(cache_dir: str | None = None):
    """Function to print available models, first those present locally."""
    if cache_dir is not None:
        CacheDir.initialize(cache_dir=cache_dir)
    registry = load_model_registry()
    ckpt_dir = CacheDir.get() / "gnn_checkpoints"

    local_models = []
    remote_models = []
    _summary = ""
    for model, info in registry.items():
        local_path = ckpt_dir / info["local"]
        kind = info["kind"]
        implemented = info.get("implemented", False)
        if implemented:
            if local_path.is_file():
                local_models.append((model, kind))
            else:
                remote_models.append((model, kind))
    if len(local_models) > 0:
        _summary += f"{'DOWNLOADED MODELS':^80}\n"
        _summary += f"{'(' + str(ckpt_dir) + ')':-^80}\n"
        for model, kind in local_models:
            _str = f"{model} ({kind})"
            _summary += f"{_str:<40}\n"

    _summary += f"{'AVAILABLE MODELS':-^80}\n"
    for model, kind in remote_models:
        _str = f"{model} ({kind})"
        _summary += f"{_str:<80}\n"
    _summary += "-" * 80
    return _summary


def get_checkpoint_path(gnn_backbone_id: str) -> Path:
    registry = load_model_registry()
    gnn_checkpoints_dir = CacheDir.get() / "gnn_checkpoints"

    if gnn_backbone_id not in registry.keys():
        raise NameError(
            f"Unknown {gnn_backbone_id} GNN backbone, the current available backbones are\n{make_summary()}"
        )
    else:
        backbone_info = registry[gnn_backbone_id]
        ckpt_path = gnn_checkpoints_dir / backbone_info["local"]
        if not ckpt_path.exists():
            download_checkpoint(gnn_backbone_id)
    return ckpt_path


def download_checkpoint(gnn_backbone_id: str, cache_dir: str | None = None) -> None:
    """Download the model if it's not already present locally."""
    registry = load_model_registry()
    if cache_dir is not None:
        CacheDir.initialize(cache_dir=cache_dir)
    ckpt_dir = CacheDir.get() / "gnn_checkpoints"

    if gnn_backbone_id not in registry.keys():
        raise NameError(
            f"Unknown {gnn_backbone_id} GNN backbone, the current available backbones are\n{make_summary()}"
        )

    if not registry[gnn_backbone_id]["implemented"]:
        raise NotImplementedError(
            f"The model {gnn_backbone_id} is not implemented in franken yet."
        )

    local_path = ckpt_dir / registry[gnn_backbone_id]["local"]
    remote_path = registry[gnn_backbone_id]["remote"]

    if local_path.is_file():
        logger.info(
            f"Model already exists locally at {local_path}. No download needed."
        )
        return

    local_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Downloading model from {remote_path} to {local_path}")
    try:
        response = requests.get(remote_path, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))

        with (
            open(local_path, "wb") as f,
            tqdm(
                desc="Downloading",
                total=total_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                ncols=100,
            ) as bar,
        ):
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                bar.update(len(chunk))
    except requests.RequestException as e:
        logger.error(f"Download failed. {e}")
        raise e


def load_checkpoint(
    gnn_backbone_id: str,
    **kwargs,
) -> torch.nn.Module:
    ckpt_path = get_checkpoint_path(gnn_backbone_id)
    registry = load_model_registry()

    backbone_family = registry[gnn_backbone_id]["kind"].lower()
    err_msg = f"franken wasn't able to load {gnn_backbone_id}. Is {backbone_family} installed?"
    if backbone_family == "fairchem":
        try:
            from franken.backbones.wrappers.fairchem_schnet import FrankenSchNetWrap
        except ImportError as import_err:
            logger.error(err_msg, exc_info=import_err)
            raise
        return FrankenSchNetWrap.load_from_checkpoint(
            str(ckpt_path), gnn_backbone_id=gnn_backbone_id, **kwargs
        )
    elif backbone_family == "mace":
        try:
            from franken.backbones.wrappers.mace_wrap import FrankenMACE
        except ImportError as import_err:
            logger.error(err_msg, exc_info=import_err)
            raise
        return FrankenMACE.load_from_checkpoint(
            str(ckpt_path), gnn_backbone_id=gnn_backbone_id, **kwargs
        )
    elif backbone_family == "sevenn":
        try:
            from franken.backbones.wrappers.sevenn import FrankenSevenn
        except ImportError as import_err:
            logger.error(err_msg, exc_info=import_err)
            raise
        return FrankenSevenn.load_from_checkpoint(
            ckpt_path, gnn_backbone_id=gnn_backbone_id, **kwargs
        )
    else:
        raise ValueError(f"Unknown backbone family {backbone_family}")
