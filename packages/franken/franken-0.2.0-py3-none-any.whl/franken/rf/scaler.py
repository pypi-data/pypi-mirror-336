import math
from typing import Any, Optional

import torch
import torch.utils.data
from tqdm import tqdm

import franken.utils.distributed as dist_utils
from franken.data import BaseAtomsDataset
from franken.utils.misc import garbage_collection_cuda


class Statistics:
    """Running statistics on a dataset, computing both per-species and global statistics."""

    def __init__(self, input_dim: Optional[int] = None):
        self.input_dim = input_dim
        self.statistics: dict[int, dict[str, Any]] = {}
        if self.input_dim is not None:
            self._initialize_statistics_for_prefix(0)  # Use 0 for global statistics

    def __call__(self, descriptors: torch.Tensor, atomic_numbers: torch.Tensor) -> None:
        """Call self.update(descriptors, atomic_numbers)"""
        self.update(descriptors, atomic_numbers)

    def update(self, descriptors: torch.Tensor, atomic_numbers: torch.Tensor) -> None:
        """
        Update running statistics for both per-species and global features.

        Args:
            descriptors: Input features of shape (n_atoms, input_dim)
            atomic_numbers: Atomic numbers for each atom
        """
        if self.input_dim is None:
            self.input_dim = descriptors.shape[1]
        assert self.input_dim == descriptors.shape[1]

        # Update global statistics (use 0 as the key)
        self._update_stats(descriptors, 0)

        # Update per-species statistics directly using atomic numbers as integer keys
        for Z in torch.unique(atomic_numbers, sorted=True):
            mask = atomic_numbers == Z
            self._update_stats(descriptors[mask], Z.item())  # Use Z as an integer key

    def _update_stats(self, x: torch.Tensor, prefix: int) -> None:
        """Update running statistics using Welford's online algorithm."""
        assert (
            x.ndim == 2 and x.shape[1] == self.input_dim
        ), f"Expected shape (n, {self.input_dim})"

        # Initialize statistics if they don't exist
        if prefix not in self.statistics:
            self._initialize_statistics_for_prefix(prefix, device=x.device)

        stats = self.statistics[prefix]

        # Compute batch statistics
        batch_size = x.shape[0]
        batch_mean = torch.mean(x, dim=0)
        batch_m2 = torch.sum((x - batch_mean) ** 2, dim=0)

        # Update running statistics (Welford's algorithm)
        new_count = stats["count"] + batch_size
        delta = batch_mean - stats["mean"]
        new_mean = stats["mean"] + delta * batch_size / new_count
        new_M2 = (
            stats["M2"]
            + batch_m2
            + delta**2 * (batch_size * stats["count"] / new_count)
        )

        # Store updated statistics
        stats["count"] = new_count
        stats["mean"] = new_mean
        stats["M2"] = new_M2
        stats["std"] = torch.sqrt(new_M2 / new_count)
        stats["min"] = torch.minimum(stats["min"], torch.min(x, dim=0).values)
        stats["max"] = torch.maximum(stats["max"], torch.max(x, dim=0).values)

    def _initialize_statistics_for_prefix(
        self, prefix: int, device: torch.device = torch.device("cpu")
    ) -> None:
        """Initialize the statistics dictionary for a given prefix if it does not exist."""
        assert self.input_dim is not None
        self.statistics[prefix] = {
            "count": 0,
            "mean": torch.zeros(self.input_dim, device=device, dtype=torch.float64),
            "M2": torch.zeros(self.input_dim, device=device, dtype=torch.float64),
            "std": torch.ones(self.input_dim, device=device, dtype=torch.float64),
            "min": torch.full(
                (self.input_dim,), float("inf"), device=device, dtype=torch.float64
            ),
            "max": torch.full(
                (self.input_dim,), float("-inf"), device=device, dtype=torch.float64
            ),
        }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.statistics.__repr__()})"

    @property
    def num_species(self):
        return len(self.statistics.keys()) - 1


class FeatureScaler(torch.nn.Module):
    def __init__(
        self,
        input_dim: int,
        statistics: Optional[Statistics],
        scale_by_Z: bool,
        num_species: int,
    ):
        super().__init__()
        self.input_dim = input_dim
        self.scale_by_Z = scale_by_Z
        self.num_species = num_species if scale_by_Z else 1
        self.Z_keys: list[int] = []

        # Initialize mean and std to default values
        self.mean: torch.Tensor
        self.std: torch.Tensor
        self.register_buffer("mean", torch.zeros(self.num_species, input_dim))
        self.register_buffer("std", torch.ones(self.num_species, input_dim))

        if statistics is not None:
            self.set_from_statistics(statistics)

    def set_from_statistics(self, statistics: Statistics):
        assert self.input_dim == statistics.input_dim
        assert self.input_dim is not None

        if self.scale_by_Z:
            # Initialize Z_keys as a sorted list of atomic numbers (excluding global 0)
            self.Z_keys = sorted(
                [key for key in statistics.statistics.keys() if key != 0]
            )
            assert len(self.Z_keys) == self.num_species

            for idx, Z in enumerate(self.Z_keys):
                self.mean[idx] = statistics.statistics[Z]["mean"].to(
                    dtype=self.mean.dtype
                )
                self.std[idx] = statistics.statistics[Z]["std"].to(dtype=self.std.dtype)
        else:
            assert self.num_species == 1
            # Use global scaling: keep mean and std as [1, input_dim]
            global_stats = statistics.statistics[0]  # Use key 0 for global
            self.mean = global_stats["mean"].view(1, -1).to(dtype=self.mean.dtype)
            self.std = global_stats["std"].view(1, -1).to(dtype=self.std.dtype)

    def forward(
        self, descriptors: torch.Tensor, atomic_numbers: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        assert descriptors.shape[1] == self.input_dim

        if not self.scale_by_Z:
            # Global scaling, simply normalize all descriptors
            return (descriptors - self.mean) / (self.std * math.sqrt(self.input_dim))

        # Normalize per atomic number (Z)
        assert atomic_numbers is not None, "atomic_numbers required when scaling by Z"
        for idx, Z in enumerate(self.Z_keys):
            mask = atomic_numbers == Z
            descriptors[mask] = (descriptors[mask] - self.mean[idx]) / (
                self.std[idx] * math.sqrt(self.input_dim)
            )
        return descriptors

    def hyperparameters(self):
        return self.init_args()

    def init_args(self):
        return {"scale_by_Z": self.scale_by_Z}

    def get_extra_state(self):
        return {"Z_keys": torch.tensor(self.Z_keys, dtype=torch.int32)}

    def set_extra_state(self, state):
        self.Z_keys = state["Z_keys"].tolist()

    def __repr__(self):
        repr = f"scale_by_Z={self.scale_by_Z}, Z_keys={self.Z_keys}, mean={self.mean.shape}, std={self.std.shape}"
        return f"{self.__class__.__name__}({repr})"


def compute_dataset_statistics(
    dataset: BaseAtomsDataset,
    gnn,
    device: torch.device,
):
    # Initialize statistics object
    gnn_features_stats = Statistics()
    pbar = tqdm(
        total=len(dataset),
        desc="Computing dataset statistics",
        disable=dist_utils.get_rank() != 0,
    )
    # Iterate over dataset and update stats
    for data, _ in dataset:  # type: ignore
        data = data.to(device=device)
        gnn_features = gnn.descriptors(data)
        gnn_features_stats.update(gnn_features, atomic_numbers=data.atomic_numbers)
        pbar.update(1)

    # Cleanup
    garbage_collection_cuda()

    return gnn_features_stats
