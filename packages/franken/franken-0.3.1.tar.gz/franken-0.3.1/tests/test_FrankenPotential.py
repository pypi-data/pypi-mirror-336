import logging
import os

os.environ["OMP_NUM_THREADS"] = "8"
from unittest.mock import DEFAULT, patch

import ase
import numpy as np
import pytest
import torch
from ase import units
from ase.io import read
from ase.md.npt import NPT
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution

from franken.calculators.ase_calc import FrankenCalculator
from franken.autotune.script import init_loaders, run_autotune
from franken.data import BaseAtomsDataset
from franken.data.base import Configuration
from franken.rf.model import FrankenPotential
from franken.rf.scaler import Statistics
from franken.trainers.rf_cuda_lowmem import RandomFeaturesTrainer
from franken.utils.misc import garbage_collection_cuda
from franken.datasets.registry import DATASET_REGISTRY

from .conftest import DEFAULT_GNN_IDS, DEVICES
from .utils import are_dicts_close, cleanup_dir, create_temp_dir, mocked_gnn

RF_PARAMETRIZE = [
    "poly",
    "gaussian",
    "linear",
    "biased-gaussian",
    "multiscale-gaussian",
]


@pytest.mark.parametrize("rf_type", RF_PARAMETRIZE)
@pytest.mark.parametrize("device", DEVICES)
def test_deterministic_initialization(rf_type, device):
    rfparams = {"rng_seed": 42} if rf_type != "linear" else {}
    for gnn_id in DEFAULT_GNN_IDS:
        # Instantiate two models with the same rng_seed
        model1 = FrankenPotential(
            gnn_id,
            rf_type,
            random_features_params=rfparams,
        ).to(device)

        model2 = FrankenPotential(
            gnn_id,
            rf_type,
            random_features_params=rfparams,
        ).to(device)

        # Compare their rf.state_dict()
        assert are_dicts_close(
            model1.rf.state_dict(), model2.rf.state_dict()
        ), f"Model initializations are not deterministic for {device=}, {gnn_id=}, {rf_type=}"


def mocked_torch_save_load():
    return patch.multiple("torch", load=DEFAULT, save=DEFAULT)


def mocked_dataset(num_atoms, dtype, device, num_configs: int = 1):
    data = []
    for _ in range(num_configs):
        data.append(
            Configuration(
                torch.randn(num_atoms, 3, dtype=dtype),
                torch.randint(1, 100, (num_atoms,)),
                torch.tensor(num_atoms),
            ).to(device)
        )
    return data


def test_load_with_legacy_gnn_arg(caplog):
    # Tests whether loading a model where gnn is specified at the base-level
    # of the checkpoint instead of within 'gnn' key
    with mocked_gnn("cpu", torch.float32, backbone_id="test"):
        model = FrankenPotential(
            gnn_backbone_id="test",
            kernel_type="gaussian"
        ).to("cpu")
        save_path = "test.pt"
        with mocked_torch_save_load() as p2:
            model.save(save_path)
            save_ckpt = p2["save"].call_args.args[0]
            assert save_ckpt is not None
            assert save_path == p2["save"].call_args.args[1]
            # Simulate the old model
            save_ckpt['gnn_backbone_id'] = 'test'
            save_ckpt['interaction_block'] = save_ckpt['gnn']['config']['interaction_block']
            del save_ckpt['gnn']
            # Now load and check
            p2["load"].return_value = save_ckpt
            with caplog.at_level(logging.WARNING):
                loaded_model = FrankenPotential.load(save_path)
            assert "Loading legacy checkpoint with limited" in caplog.text
            assert loaded_model.gnn.init_args() == {
                "gnn_backbone_id": "test",
                "interaction_block": 2,
            }


def test_load_with_rf_dtype_arg(caplog):
    # Tests whether loading a model where rf has dtype parameter specified still works.
    # Since the dtype parameter was removed this should just give a warning.
    with mocked_gnn("cpu", torch.float32, backbone_id="test"):
        model = FrankenPotential(
            gnn_backbone_id="test",
            kernel_type="gaussian"
        ).to("cpu")
        save_path = "test.pt"
        with mocked_torch_save_load() as p2:
            model.save(save_path)
            save_ckpt = p2["save"].call_args.args[0]
            assert save_ckpt is not None
            assert save_path == p2["save"].call_args.args[1]
            # Set the dtype argument to simulate an old model
            save_ckpt["rf"]["config"]["dtype"] = torch.float64
            # Now load and check that it only gives a warning
            p2["load"].return_value = save_ckpt
            # NOTE: caplog is a default fixture which allows to capture
            #       the outputs of the logging module.
            with caplog.at_level(logging.WARNING):
                loaded_model = FrankenPotential.load(save_path)
            assert "invalid parameters: {'dtype'" in caplog.text
            assert "dtype" not in loaded_model.rf.init_args()


@pytest.mark.parametrize("rf_type", RF_PARAMETRIZE)
@pytest.mark.parametrize("device", DEVICES)
@pytest.mark.parametrize("scale_by_Z", [True, False])
def test_save_load_functionality(rf_type, device, scale_by_Z):
    """Test for checking save and load methods of FrankenPotential"""
    for gnn_id in DEFAULT_GNN_IDS:
        temp_dir = None
        try:
            # Step 1: Create a temporary directory for saving the model
            temp_dir = create_temp_dir()

            data_path = DATASET_REGISTRY.get_path("test", "test", None, False)
            dataset = BaseAtomsDataset.from_path(
                data_path=data_path,
                split="train",
                gnn_backbone_id=gnn_id,
            )

            model = FrankenPotential(
                gnn_backbone_id=gnn_id,
                kernel_type=rf_type,
                random_features_params={},
                scale_by_Z=scale_by_Z,
                num_species=dataset.num_species,
            ).to(device)

            with torch.no_grad():
                gnn_features_stats = Statistics()
                for data, _ in dataset:  # type: ignore
                    data = data.to(device=device)
                    gnn_features = model.gnn.descriptors(data)
                    gnn_features_stats.update(
                        gnn_features, atomic_numbers=data.atomic_numbers
                    )

                model.input_scaler.set_from_statistics(gnn_features_stats)
                garbage_collection_cuda()

            # Step 2: Save the model to the temporary directory
            model_save_path = os.path.join(temp_dir, "model_checkpoint.pth")
            model.save(model_save_path)

            # Step 3: Load the model from the saved checkpoint
            loaded_model = FrankenPotential.load(model_save_path, map_location=device)

            # Step 4: Compare rf.state_dict between the original and loaded models
            assert are_dicts_close(
                model.rf.state_dict(), loaded_model.rf.state_dict(), verbose=True
            ), "The rf.state_dict() of the loaded model does not match the original model."
            assert are_dicts_close(
                model.input_scaler.state_dict(),
                loaded_model.input_scaler.state_dict(),
                verbose=True,
            ), "The input_scaler.state_dict() of the loaded model does not match the original model."

            # Step 5: Compare the hyperparameters between the original and loaded models
            assert (
                model.hyperparameters == loaded_model.hyperparameters
            ), "The hyperparameters of the loaded model do not match the original model."
        finally:
            if temp_dir is not None:
                cleanup_dir(temp_dir)


@pytest.mark.parametrize("rf_type", RF_PARAMETRIZE)
@pytest.mark.parametrize("device", DEVICES)
@pytest.mark.parametrize("scale_by_Z", [True, False])
def test_multiweight_save_load_functionality(rf_type, device, scale_by_Z):
    """Test for checking save and load methods of FrankenPotential"""
    for gnn_id in DEFAULT_GNN_IDS:
        temp_dir = None
        try:
            # Step 1: Create a temporary directory for saving the model
            temp_dir = create_temp_dir()

            data_path = DATASET_REGISTRY.get_path("test", "test", None, False)
            dataset = BaseAtomsDataset.from_path(
                data_path=data_path,
                split="train",
                gnn_backbone_id=gnn_id,
            )

            model = FrankenPotential(
                gnn_id,
                rf_type,
                random_features_params={},
                scale_by_Z=scale_by_Z,
                num_species=dataset.num_species,
            ).to(device)

            with torch.no_grad():
                gnn_features_stats = Statistics()
                for data, _ in dataset:  # type: ignore
                    data = data.to(device=device)
                    gnn_features = model.gnn.descriptors(data)
                    gnn_features_stats.update(
                        gnn_features, atomic_numbers=data.atomic_numbers
                    )

                model.input_scaler.set_from_statistics(gnn_features_stats)
                garbage_collection_cuda()

            multi_weights = torch.randn(
                17, model.rf.total_random_features, device=device, dtype=torch.float64
            )

            # Step 2: Save the model to the temporary directory
            model_save_path = os.path.join(temp_dir, "model_checkpoint.pth")
            model.save(model_save_path, multi_weights)

            # Step 3: Load the model from the saved checkpoint
            loaded_model = FrankenPotential.load(
                model_save_path,
                map_location=device,
                rf_weight_id=10,
            )

            model.rf.weights.copy_(multi_weights[10].reshape_as(model.rf.weights))

            # Step 4: Compare rf.state_dict between the original and loaded models
            assert are_dicts_close(
                model.rf.state_dict(), loaded_model.rf.state_dict(), verbose=True
            ), "The rf.state_dict() of the loaded model does not match the original model."

            # Step 5: Compare the hyperparameters between the original and loaded models
            assert (
                model.hyperparameters == loaded_model.hyperparameters
            ), "The hyperparameters of the loaded model do not match the original model."
        finally:
            if temp_dir is not None:
                cleanup_dir(temp_dir)


@pytest.mark.parametrize("rf_type", RF_PARAMETRIZE)
@pytest.mark.parametrize("device", DEVICES)
@pytest.mark.parametrize("multiweights", [True, False])
def test_inference_force_mode(rf_type, device, multiweights: bool):
    for gnn_id in DEFAULT_GNN_IDS:
        data_path = DATASET_REGISTRY.get_path("test", "test", None, False)
        dataset = BaseAtomsDataset.from_path(
            data_path=data_path,
            split="train",
            gnn_backbone_id=gnn_id,
            num_random_subsamples=1,
        )

        model = FrankenPotential(
            gnn_id,
            rf_type,
            random_features_params={},
            scale_by_Z=True,
            num_species=dataset.num_species,
        ).to(device)

        if multiweights:
            dummy_multiweights = torch.randn(
                (10,) + model.rf.weights.shape,
                dtype=model.rf.weights.dtype,
                device=model.rf.weights.device,
            )
            model.rf.weights = dummy_multiweights
        else:
            model.rf.weights.copy_(torch.randn(model.rf.weights.shape))

        calc_func = FrankenCalculator(model, device=device, forces_mode="torch.func")
        calc_autograd = FrankenCalculator(
            model,
            device=device,
            forces_mode="torch.autograd",
        )
        for atoms in dataset.ase_atoms[:1]:
            calc_func.calculate(atoms)
            calc_autograd.calculate(atoms)
            print(
                np.max(
                    np.abs(
                        calc_func.results["forces"] - calc_autograd.results["forces"]
                    )
                )
            )
            assert np.allclose(
                calc_func.results["forces"],
                calc_autograd.results["forces"],
                rtol=1e-3,
                atol=1e-3,
            )
            assert np.allclose(
                calc_func.results["energy"],
                calc_autograd.results["energy"],
                rtol=1e-3,
                atol=1e-3,
            )


@pytest.mark.parametrize("rf_type", RF_PARAMETRIZE)
@pytest.mark.parametrize("device", DEVICES)
@pytest.mark.parametrize("multiweights", [True, False])
class TestModelGradients:
    def test_gradients_mocked(self, rf_type, device, multiweights):
        num_atoms = 10
        dtype = torch.float32
        with mocked_gnn(device=device, dtype=dtype, feature_dim=32):
            model = FrankenPotential(
                "test",
                rf_type,
                random_features_params={},
            ).to(device)

        num_lin_models = 10 if multiweights else 1
        weights = torch.randn(
            (num_lin_models, model.rf.total_random_features), device=device
        )
        data = Configuration(
            torch.randn(num_atoms, 3, dtype=dtype),
            torch.randint(1, 100, (num_atoms,)),
            torch.tensor(num_atoms),
        ).to(device)
        energy_autograd, forces_autograd = model.energy_and_forces(
            data, weights=weights, forces_mode="torch.autograd"
        )
        energy_func, forces_func = model.energy_and_forces(
            data, weights=weights, forces_mode="torch.func"
        )
        torch.testing.assert_close(energy_func, energy_autograd, rtol=1e-3, atol=1e-3)
        torch.testing.assert_close(forces_func, forces_autograd, rtol=1e-3, atol=1e-3)

    @pytest.mark.parametrize("gnn_id", DEFAULT_GNN_IDS)
    def test_gradients_real(self, rf_type, device, multiweights: bool, gnn_id):
        # Define the rng_seed and initialize the model
        model = FrankenPotential(
            gnn_id,
            rf_type,
            random_features_params={},
        ).to(device)

        num_lin_models = 10 if multiweights else 1
        weights = torch.randn(
            (num_lin_models, model.rf.total_random_features), device=device
        )
        data_path = DATASET_REGISTRY.get_path("test", "test", None, False)
        dataset = BaseAtomsDataset.from_path(
            data_path=data_path,
            split="train",
            gnn_backbone_id=gnn_id,
        )
        data, _ = dataset[0]  # type: ignore
        data = data.to(device)
        energy_autograd, forces_autograd = model.energy_and_forces(
            data, weights=weights, forces_mode="torch.autograd"
        )
        energy_func, forces_func = model.energy_and_forces(
            data, weights=weights, forces_mode="torch.func"
        )
        torch.testing.assert_close(energy_func, energy_autograd, rtol=1e-3, atol=1e-3)
        torch.testing.assert_close(forces_func, forces_autograd, rtol=1e-3, atol=1e-3)


@pytest.mark.parametrize("rf_type", RF_PARAMETRIZE)
@pytest.mark.parametrize("device", DEVICES)
@pytest.mark.parametrize("gnn_id", DEFAULT_GNN_IDS)
def test_calculator_in_md(rf_type, device, gnn_id):
    # Define the rng_seed and initialize the model
    model = FrankenPotential(
        gnn_id,
        rf_type,
        random_features_params={},
    ).to(device)
    num_lin_models = 1  # only a single weight for MD
    rf_weights = torch.randn(
        (num_lin_models, model.rf.total_random_features), device=device
    )
    model.rf.weights = rf_weights
    calculator = FrankenCalculator(model, device=device, forces_mode="torch.autograd")

    # Molecular dynamics
    # 1. Get the initial configuration
    # 2. Set some attribute on the configuration with MaxwellBoltzmannDistribution
    # 3. Create and run the MD
    data_path = DATASET_REGISTRY.get_path("test", "md", None, False)

    init_traj_atoms = read(data_path, index=0)
    assert isinstance(init_traj_atoms, ase.Atoms)
    init_traj_atoms.calc = calculator
    MaxwellBoltzmannDistribution(init_traj_atoms, temperature_K=500)
    md = NPT(
        init_traj_atoms,
        timestep=1 * units.fs,
        temperature_K=500,
        ttime=25 * units.fs,
        logfile="-",
        trajectory=None,
        loginterval=1,
    )
    md.run(2)


@pytest.mark.parametrize("rf_type", RF_PARAMETRIZE)
@pytest.mark.parametrize("gnn_id", DEFAULT_GNN_IDS)
@pytest.mark.parametrize("device", DEVICES)
@pytest.mark.parametrize("atomic_energies", [None, {7: 1.0, 26: 10.0}])
def test_autotune(rf_type, gnn_id, device, atomic_energies):
    loaders = init_loaders(
        gnn_id,
        DATASET_REGISTRY.get_path("test", "train", None, False),
        test_path=DATASET_REGISTRY.get_path("test", "test", None, False),
        val_path=DATASET_REGISTRY.get_path("test", "val", None, False),
    )
    trainer = RandomFeaturesTrainer(
        train_dataloader=loaders["train"],
        random_features_normalization=None,
        log_dir=None,  # TODO: Test with log_dir not None (but mocked) since there was a regression here
        save_every_model=False,
        device=device,
    )
    rf_hp_grid = [
        (
            0,
            {
                "num_random_features": 256,
                "length_scale": 1.0,
            },
        ),
        (
            1,
            {
                "num_random_features": 512,
                "length_scale": 1.0,
            },
        ),
    ]
    solver_hp_grid = {
        "L2_penalty": [1e-8],
        "loss_lerp_weight": [0.1, 0.9],
    }
    best_model = run_autotune(
        rnd_seed=42,
        gnn_backbone_id=gnn_id,
        interaction_block=2,
        rf_type=rf_type,
        loaders=loaders,
        rf_param_grid=rf_hp_grid,
        solver_param_grid=solver_hp_grid,
        trainer=trainer,
        scale_by_Z=False,
        atomic_energies=atomic_energies,
        jac_chunk_size="auto",
    )
    print(best_model)
    # TODO: Assert something to prevent regressions


class TestStatistics:
    def test_online_algo(self):
        dim = 128
        atomic_numbers = torch.tensor([1, 5, 1])
        data = torch.randn(100, len(atomic_numbers), dim)
        st = Statistics(input_dim=dim)

        for data_item in data:
            st.update(data_item, atomic_numbers)

        # Compute the expected values
        global_mean = data.view(-1, dim).mean(0)
        global_std = data.view(-1, dim).std(0)

        torch.testing.assert_close(st.statistics[0]["mean"], global_mean.double())
        torch.testing.assert_close(
            st.statistics[0]["std"], global_std.double(), rtol=1e-2, atol=1e-2
        )

    def test_per_atom(self):
        dim = 128
        atomic_numbers = torch.tensor([1, 5, 1])
        data = torch.randn(100, len(atomic_numbers), dim)
        st = Statistics(input_dim=dim)

        for data_item in data:
            st.update(data_item, atomic_numbers)

        # Compute the expected values
        atom1_mean = data[:, [0, 2]].view(-1, dim).mean(0)
        atom5_mean = data[:, [1]].view(-1, dim).mean(0)
        atom1_std = data[:, [0, 2]].view(-1, dim).std(0)
        atom5_std = data[:, [1]].view(-1, dim).std(0)

        torch.testing.assert_close(st.statistics[1]["mean"], atom1_mean.double())
        torch.testing.assert_close(
            st.statistics[1]["std"], atom1_std.double(), rtol=1e-2, atol=1e-2
        )
        torch.testing.assert_close(st.statistics[5]["mean"], atom5_mean.double())
        torch.testing.assert_close(
            st.statistics[5]["std"], atom5_std.double(), rtol=1e-2, atol=1e-2
        )


class TestFit:
    pass


class TestSerialize:
    pass
