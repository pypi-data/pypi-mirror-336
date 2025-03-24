from ase.io import read, write

if __name__ == "__main__":
    # Loading the dataset
    dataset = read("ML_AB_dataset_2.xyz", index=":", format="extxyz")
    # Saving new dataset
    write("ML_AB_dataset_2-val.xyz", dataset[473:])
