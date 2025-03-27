from pathlib import Path
import time
from typing import Literal, Union

import numpy as np
import torch

from ase.calculators.calculator import Calculator, all_changes
import ase.io
from franken.data import BaseAtomsDataset, Configuration
from franken.rf.model import FrankenPotential
from franken.utils.misc import get_device_name


def run(franken_ckpt, device, traj_path, num_reps=100):
    franken = FrankenPotential.load(
        franken_ckpt,
        map_location=device,
        rf_weight_id=None,
    )
    dataset = BaseAtomsDataset.from_path(
        data_path=None,
        split="md",
        gnn_backbone_id=franken.gnn_backbone_id,
    )
    atoms = ase.io.read(traj_path, index=0)

    config_idx = dataset.add_configuration(atoms)  # type: ignore
    cpu_data = dataset.__getitem__(config_idx, no_targets=True)
    assert isinstance(cpu_data, Configuration)
    data = cpu_data.to(device)
    t_iter = []
    for rep in range(num_reps):
        t_s = time.time()
        energy, forces = franken.energy_and_forces(data, forces_mode="torch.autograd")
        energy = energy.cpu()
        if forces is not None:
            forces = forces.cpu()
        t_iter.append(time.time() - t_s)
    print(f"Took {np.mean(t_iter):.2f}s average time")


if __name__ == "__main__":
    franken_ckpt = "/leonardo_work/IIT24_AtomSim/franken_data/experiments/water/multinode_test/test2/run_250108_175820_2f84bf52/best_ckpt.pt"
    device = "cuda:0"
    traj_path = "/leonardo/home/userexternal/gmeanti0/mlpot_transfer/datasets/water/ML_AB_dataset_1.xyz"

    run(franken_ckpt, device, traj_path)

