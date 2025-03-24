from ase.io import read, write
from numpy.random import shuffle, seed


if __name__ == "__main__":
    traj = read("dataset.traj", index=":")

    seed(42)
    shuffle(traj)

    train = traj[:30000]
    valid = traj[30000:31000]
    test = traj[31000:]

    write("train.extxyz", train)
    write("valid.extxyz", valid)
    write("test.extxyz", test)
