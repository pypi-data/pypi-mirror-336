import logging
import weakref
from typing import Any

from omegaconf import OmegaConf
import ase.md.md
import ase.units
from ase import Atoms
import numpy as np

from franken.mdgen.tm23_utils import tm23_temp
from franken import FRANKEN_DIR


logger = logging.getLogger("franken")


class MDError(RuntimeError):
    pass


def get_md_nan_checker(atoms: Atoms):
    def check_nans():
        # Forces are not set as an attribute on the atoms.
        # Therefore we check the positions which should be derived
        # from the forces (and therefore NaNs should be propagated)
        forces = atoms.get_forces()
        if not np.all(np.isfinite(forces)):
            raise MDError("Inf/NaN values encountered in atomic forces")
        energy = atoms.get_potential_energy()
        if not np.all(np.isfinite(energy)):
            raise MDError("Inf/NaN values encountered in atomic energies")

    return check_nans


class FrankenMDLogger:
    def __init__(
        self,
        dynamics: ase.md.md.MolecularDynamics,
        atoms: Atoms,
        stress: bool,
        peratom: bool,
    ):
        self.dynamics = (
            weakref.proxy(dynamics) if hasattr(dynamics, "get_time") else None
        )
        self.atoms = atoms
        global_natoms = atoms.get_global_number_of_atoms()
        self.stress = stress
        self.peratom = peratom
        self.logged_data: list[dict[str, Any]] = []
        self.hdr = ""
        self.fmt = ""
        if self.dynamics is not None:
            self.hdr = f"{'Time[ps]':10s} "
            self.fmt = "{:<10.4f} "
        if self.peratom:
            self.hdr += (
                f"{'Etot/N[eV]':12s} {'Epot/N[eV]':12s} {'Ekin/N[eV]':12s} {'T[K]':6s}"
            )
            self.fmt += "{:<12.4f} {:<12.4f} {:<12.4f} {:<6.1f}"
        else:
            self.hdr += (
                f"{'Etot[eV]':12s} {'Epot[eV]':12s} {'Ekin[eV]':12s} {'T[K]':6s}"
            )
            # Choose a sensible number of decimals
            if global_natoms <= 100:
                digits = 4
            elif global_natoms <= 1000:
                digits = 3
            elif global_natoms <= 10000:
                digits = 2
            else:
                digits = 1
            self.fmt += 3 * f"{{:<12.{digits}f}} " + "{:<6.1f}"

        if self.stress:
            self.hdr += (
                "      ---------------------- stress [GPa] " "-----------------------"
            )
            self.fmt += 6 * " {:<10.3f}"
        logger.info(self.hdr)

    def __call__(self):
        data_item = {}
        epot = self.atoms.get_potential_energy()
        ekin = self.atoms.get_kinetic_energy()
        temp = self.atoms.get_temperature()

        global_natoms = self.atoms.get_global_number_of_atoms()
        if self.peratom:
            epot /= global_natoms
            ekin /= global_natoms
        if self.dynamics is not None:
            t = self.dynamics.get_time() / (1000 * ase.units.fs)
            dat = [
                t,
            ]
            data_item["time"] = t
        else:
            dat = []

        data_item["epot"] = epot
        data_item["ekin"] = ekin
        data_item["temp"] = temp

        dat += [epot + ekin, float(epot), ekin, temp]

        if self.stress:
            dat += list(self.atoms.get_stress(include_ideal_gas=True) / ase.units.GPa)

        self.logged_data.append(data_item)
        logger.info(self.fmt.format(*dat))


def register_hydra_resolvers():
    OmegaConf.register_new_resolver("fs_to_ase", lambda x: float(x) * ase.units.fs)
    OmegaConf.register_new_resolver("invfs_to_ase", lambda x: float(x) / ase.units.fs)
    OmegaConf.register_new_resolver("tm23_temp", tm23_temp)
    # TODO: Not sure this will work when franken is pip-installed
    OmegaConf.register_new_resolver(
        "default_datasets_path",
        lambda: str((FRANKEN_DIR.parent / "datasets").resolve()),
    )
