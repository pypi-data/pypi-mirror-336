# Franken MD Simulations

## Running MD on TM23 data

### Starting MD simulation

Assuming we have trained a Franken model at `best_ckpt.pt` this is enough to start a default simulation.
```
franken.mdgen \
    md=TM23 \
    element=Ag \
    temperature_label=cold \
    calculator.model_path=best_ckpt.pt
```

### Postprocessing basics
For postprocessing of the simulations which resulted from the previous run you should run
```
franken.mdgen.postprocess \
    postprocess=TM23 \
    element=Ag \
    temperature_label=cold
```

### Custom experiment name

The experiment output directory is going to be built as `${root_dir}/md/${exp_name}` where `root_dir` is the directory you're launching the experiment from and `exp_name` is a configuration variable. If you wish to rerun another experiment on the same data but with different parameters, make sure to specify the `exp_name` variable in order not to override the default, for example (MD and postprocess)
```
franken.mdgen \
    md=TM23 \
    element=Ag \
    temperature_label=cold \
    timestep_fs=1.0 \
    calculator.model_path=best_ckpt.pt \
    exp_name="Ag_cold_1fs"

franken.mdgen.postprocess \
    postprocess=TM23 \
    element=Ag \
    temperature_label=cold \
    exp_name="Ag_cold_1fs"
```

the postprocessing outputs will be saved in the same location as the MD outputs.


PYTHONPATH='.' python franken/mdgen \
    md=TM23 \
    element=Ag \
    temperature_label=cold \
    md_length_ns=0.002 \
    calculator.model_path=/scratch/clear/gmeanti/mlpot/experiments/TM23/Cr/MACE-L0/4096_rfs/gaussian/50smpl_rep1_241127_104423_c56cda2f/best_ckpt.pt

### Overriding dataset location

The default dataset location is the `franken/datasets` folder from the root of this repository.
It can be configured using the `paths.dataset_dir` configuration key, so for example if `"/ml_potentials/datasets/"` contains your TM23 data folder, you should call
```
franken.mdgen \
    md=TM23 \
    element=Ag \
    temperature_label=cold \
    calculator.model_path=best_ckpt.pt \
    paths.dataset_dir="/ml_potentials/datasets/"
```
to load the dataset from there.