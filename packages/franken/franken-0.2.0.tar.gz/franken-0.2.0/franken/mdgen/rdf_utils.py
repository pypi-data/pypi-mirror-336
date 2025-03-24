import logging
from typing import List, Literal, Optional, Tuple, Union
from ase import Atoms
from ase.geometry.rdf import get_rdf
import numpy as np
import numpy.typing as npt

import psutil
import torch

logger = logging.getLogger("franken")


def batched_distance_matrix(traj: list[Atoms], num_cells=1) -> np.ndarray:
    """From 'forces are not enough', computes distance matrix between atom positions
    dealing with non-cubic cell.

    TODO: This is likely to fail in some cases as dealing with periodic systems
          is less robust than ASE! We could switch to doing this with ase `get_distances`

    TODO: This only works if using PBC on all 3 axes
    """

    ### Batching calculations
    def max_ram(traj_len):
        # Final multiplier should be *3, becomes *4 to include reduced dist and *5
        # for safety buffer.
        return 4 * traj_len * len(traj[0]) * len(traj[0]) * (num_cells * 2 + 1) ** 3 * 5

    if torch.cuda.is_available():
        avail_ram = torch.cuda.mem_get_info()[0] * 0.9
        dev = "cuda"
    else:
        avail_ram = psutil.virtual_memory().available * 0.4
        dev = "cpu"
    batch_size = len(traj)
    while max_ram(batch_size) > avail_ram:
        logger.debug(
            f"Available {avail_ram / 2 ** 30:.2f}GiB not enough "
            f"for batch size {batch_size} (needs "
            f"{max_ram(batch_size) / 2 ** 30:.2f}GiB)"
        )
        batch_size //= 2
    logger.debug(f"Chosen batch size {batch_size}")

    ### Batch-invariant quantities
    # Extract all atom positions: [N, A, 3]
    coords = (
        torch.stack([torch.from_numpy(a.get_positions(wrap=True)) for a in traj], dim=0)
        .float()
        .to(device=dev)
    )
    # Cell is [3, 3] containing size of unit cell. cells is [N, 3, 3]
    cells = torch.stack(
        [torch.from_numpy(frame.cell.array).float() for frame in traj], 0
    ).to(device=dev)
    # If num_cells = 1, pos = -1, 0, 1: the shifts of the unit cell to be
    # considered. Call the number of positions P (in the example above P=3)
    pos = torch.arange(-num_cells, num_cells + 1, 1, device=dev)
    # combos is all possible combinations of `pos` in the 3 xyz dimensions. [P^3, 3].
    # for example there will be [-1, -1, -1], [-1, 0, -1], [1, 1, 1], etc
    combos = (
        torch.stack(torch.meshgrid(pos, pos, pos, indexing="xy"))
        .permute(3, 2, 1, 0)
        .reshape(-1, 3)
        .to(cells.device)
    )
    # and shifts is the actual shifts in cell units
    # cells * combos is [N, P^3, 3, 3],  shifts is [N, P^3, 3]
    shifts = torch.sum(cells[:, None, :, :] * combos[None, :, :, None], dim=-1)

    ### Compute batched distances
    all_dist = []
    for batch_start in range(0, len(traj), batch_size):
        # b_coords: [N, A, 3]
        b_coords = coords[batch_start : batch_start + batch_size]
        b_shifts = shifts[batch_start : batch_start + batch_size]
        # the coordinates get shifted by each of the shift: [N, A, P^3, 3]
        shifted = b_coords[:, :, None, :] + b_shifts[:, None, :, :]
        # Euclidean distance between atom positions and all shifted atom positions
        # [N, A, A, P^3, 3] -> [N, A, A, P^3]
        dist = b_coords.unsqueeze(2).unsqueeze(2) - shifted.unsqueeze(1)
        dist = torch.linalg.vector_norm(dist, ord=2, dim=-1)
        # Minimum distance among all shifted positions (Minimum-image convention)
        # [N, A, A]
        dist = dist.min(dim=-1)[0]
        all_dist.append(dist)
    return torch.cat(all_dist, 0).numpy(force=True)


def ase_distance_matrix(traj: list[Atoms]) -> npt.NDArray[np.float32]:
    dist: List[npt.NDArray[np.float32]] = []
    for config in traj:
        dist.append(config.get_all_distances(mic=True).astype(np.float32))
    return np.stack(dist, 0)


def distance_matrix(
    traj: list[Atoms], version: Literal["ase", "fast"]
) -> npt.NDArray[np.float32]:
    if version == "ase":
        return ase_distance_matrix(traj)
    elif version == "fast":
        return batched_distance_matrix(traj)
    else:
        raise RuntimeError(
            f"distance matrix implementation '{version}' not understood."
        )


def fast_avg_rdf(
    traj: list[Atoms],
    rmax: float,
    nbins: int,
    no_dists: bool = False,
    distance_matrix: np.ndarray | None = None,
    elements=None,
) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
    if distance_matrix is None:
        distance_matrix = batched_distance_matrix(traj)
    cell_volumes = np.array([frame.cell.volume for frame in traj])
    bins = np.linspace(0, rmax, nbins + 1)

    # atom-types must be uniform throughout the trajectory, otherwise use 'ase' version
    atom_types = traj[0].numbers
    for frame in traj:
        if not (atom_types == frame.numbers).all():
            raise NotImplementedError(
                "Trajectory does not have uniform atomic types or number of atoms. "
                "This cannot be handled by the fast RDF calculator, please use the 'ase' RDF version."
            )

    if elements is not None:
        # Fetch the portion of the distance matrix which concerns the two
        # chosen atomic types
        indices0 = atom_types == elements[0]
        indices1 = atom_types == elements[1]
        distance_matrix = distance_matrix.transpose(1, 2, 0)[
            np.ix_(indices0, indices1)
        ].transpose(2, 0, 1)

    rep_cell_volumes = np.repeat(
        cell_volumes, distance_matrix.shape[1] * distance_matrix.shape[2]
    )
    flat_pdist = distance_matrix.flatten()
    data_shape = flat_pdist.shape[0]

    nz_dist_mask = flat_pdist != 0
    rep_cell_volumes = rep_cell_volumes[nz_dist_mask]
    flat_pdist = flat_pdist[nz_dist_mask]
    data_hist, _ = np.histogram(flat_pdist, bins, weights=rep_cell_volumes)

    rho_data = data_shape
    Z_data = rho_data * 4 / 3 * np.pi * (bins[1:] ** 3 - bins[:-1] ** 3)
    rdf = data_hist / Z_data
    if no_dists:
        return rdf
    return rdf, np.arange(float(rmax / nbins) / 2, rmax, float(rmax / nbins))


def ase_avg_rdf(
    traj: list[Atoms],
    no_dists=False,
    distance_matrix: np.ndarray | None = None,
    elements=None,
    **kwargs,
) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
    """Calculate average RDF with ASE."""
    dists = None
    rdf_list = []
    for i, atoms in enumerate(traj):
        # NOTE: `get_rdf` is a very slow way to compute a histogram
        #       as it loops over each bin in python. We might consider
        #       changing this if performance is a problem.
        rdf, dists = get_rdf(
            atoms,
            distance_matrix=distance_matrix[i] if distance_matrix is not None else None,
            no_dists=False,
            elements=elements,
            **kwargs,
        )
        rdf_list.append(rdf)
    avg_rdf = np.mean(rdf_list, axis=0)
    if no_dists:
        return avg_rdf
    return avg_rdf, dists  # type: ignore


def avg_rdf(
    traj: list[Atoms],
    rmax: float,
    nbins: int,
    no_dists: bool = False,
    distance_matrix: np.ndarray | None = None,
    elements: Optional[Tuple[int, int]] = None,
    version: Literal["ase", "fast"] = "fast",
) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
    if version == "ase":
        return ase_avg_rdf(
            traj,
            rmax=rmax,
            nbins=nbins,
            no_dists=no_dists,
            distance_matrix=distance_matrix,
            elements=elements,
        )
    elif version == "fast":
        return fast_avg_rdf(
            traj,
            rmax=rmax,
            nbins=nbins,
            no_dists=no_dists,
            distance_matrix=distance_matrix,
            elements=elements,
        )
    else:
        raise RuntimeError(f"average RDF implementation '{version}' not understood.")


def compute_rdf_mae(rdf: np.ndarray, ref_rdf: np.ndarray, delta_r: float):
    """MAE between RDFs"""
    return np.sum(np.abs(rdf - ref_rdf)) * delta_r


def stability_rdf(
    traj: list[Atoms],
    dist: np.ndarray,
    ref_rdf: np.ndarray,
    rmax: float,
    nbins: int,
    threshold=1.0,
    stability_interval=20,
    elements: Optional[Tuple[int, int]] = None,
    rdf_version: Literal["fast", "ase"] = "fast",
):
    """Calculate RDF stability metrics between a test trajectory and a reference trajectory

    The test RDF is computed on a sliding window along the test trajectory, and compared
    using the MAE metric to the full reference RDF. If the threshold is exceeded, the test
    trajectory is deemed unstable and computations are interrupted.
    """
    stability_mae = []
    unstable_time = len(traj)  # index of first point which is unstable
    # NOTE: This was changed from computing stability once every `stability_interval`
    #       to computing it every time-step on windows of size `stability_interval`.
    #       this is consistent with 'forces are not enough'.
    for i in range(1, len(traj) - stability_interval):
        current_interval = slice(i, i + stability_interval)
        current_rdf = avg_rdf(
            traj[current_interval],
            distance_matrix=dist[current_interval],
            rmax=rmax,
            nbins=nbins,
            no_dists=True,
            version=rdf_version,
            elements=elements,
        )
        assert isinstance(current_rdf, np.ndarray)
        current_mae = compute_rdf_mae(current_rdf, ref_rdf, rmax / nbins)
        stability_mae.append(current_mae)
        if current_mae > threshold:
            unstable_time = i
            logger.warning(f"Trajectory becomes unstable at time {i}")
            break
    return unstable_time, stability_mae
