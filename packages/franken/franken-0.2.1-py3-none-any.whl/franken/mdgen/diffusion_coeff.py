from typing import Tuple
import typing
import math

import numpy as np
from scipy.stats import linregress


def calc_water_msd(traj):
    """Compute mean squared displacement on the given trajectory

    The MSD is computed at different lag-times, from zero to half the trajectory length,
    such that each MSD is computed averaging over the same number of origins.

    Notes:
    see https://www.utkstair.org/clausius/docs/che548/pdf/selfd.pdf for a discussion
    on practical details with computing the MSD and self-diffusion coefficient

    The algorithm has quadratic complexity in the trajectory length. Faster algorithms
    are possible (see [MDAnalysis](https://docs.mdanalysis.org/stable/documentation_pages/analysis/msd.html)
    for an implementation), but unnecessary unless dealing with very long trajectories.
    """
    t_max = len(traj) // 2
    max_origin = t_max
    msd = np.zeros((t_max, 3))

    # Assume water so MSD is between the oxygen atoms, which are the centers-of-mass of
    # each water molecule in the image
    o_atoms = [atoms[atoms.get_atomic_numbers() == 8] for atoms in traj]
    for origin in range(0, max_origin):
        reference = o_atoms[origin].positions
        for delta_t in range(1, t_max):
            msd[delta_t] += np.mean(
                (o_atoms[origin + delta_t].positions - reference) ** 2, axis=0
            )
    msd /= max_origin
    return msd


def calc_self_diffusion(
    msd, delta_t_fs: float, t_min: int | None = 0, t_min_fs: float | None = None
) -> Tuple[list[float], list[typing.NamedTuple]]:
    """Compute the self-diffusion coefficient from MSD data.

    Args:
        msd (np.ndarray): mean squared displacement as returned by for e.g. :func:`calc_water_msd`
        delta_t_fs (float): the time interval in femtoseconds between successive entries in the MSD
        t_min (int | None): the amount of lag-times to discard from the beginning of msd, mutually
            exclusive with specifying `t_min_fs`.
        t_min_fs (float | None): the amount of lag-times to discard from the beginning of msd
            in femtoseconds. Mutually exclusive with specifying `t_min`.

    Returns:
        Ds (list[float]): the self diffusion coefficient for each coordinate
        linmodels (list[float]): the slopes of the linear fit on the MSD
        intercepts (list[float]): the intercept of the linear fit on the MSD
    """
    t_max = msd.shape[0]

    lagtimes = np.arange(t_max)
    lagtimes_fs = lagtimes * delta_t_fs

    if t_min is None and t_min_fs is not None:
        t_min = int(math.floor(t_min_fs / delta_t_fs))
    elif t_min is None:
        t_min = 0
    linear_models = [
        linregress(lagtimes_fs[t_min:], msd[t_min:, i]) for i in range(msd.shape[1])
    ]
    Ds = [linmod.slope * 1e4 / 2 for linmod in linear_models]
    return Ds, linear_models  # type: ignore
