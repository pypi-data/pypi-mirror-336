import sys
import numpy as np
from ase.io import read

def mad(data, axis=None):
  """
  Calculates the Mean Absolute Deviation (MAD) of a dataset.

  Args:
    data: The input data as a NumPy array or list.
    axis: The axis along which to compute the MAD. 
          If None, compute the MAD over the entire array.

  Returns:
    The Mean Absolute Deviation of the data.
  """
  return np.mean(np.absolute(data - np.mean(data, axis)), axis)

def analyze_trajectory(filename):
  """
  Calculates and prints the MAD of energy and forces for an ASE trajectory.
  Saves the results to a file.

  Args:
    filename: Path to the .xyz trajectory file.
    output_filename: Name of the output file to save the results.
  """
  traj = read(filename, index=":")  # Read the entire trajectory

  energies = np.array([atoms.get_potential_energy() for atoms in traj])
  forces = np.concatenate([atoms.get_forces() for atoms in traj])

  mad_energy = mad(energies)
  mad_forces = mad(forces)
  print("Warning: Script assumes energy values are in eV and Forces in eV/Å, which is the main convention in franken, otherwise ignore units.")
  print(f"Mean Absolute Deviation of Energy: {mad_energy:.4f} eV")
  print(f"Mean Absolute Deviation of Forces: {mad_forces:.4f} eV/Å")
  output_filename = filename.split(".")[0]
  # Save results to file
  with open(output_filename+"_metrics.txt", "w") as f:
    f.write("# Property\tMAD\n")
    f.write(f"Energy (eV)\t{mad_energy:.4f}\n")
    f.write(f"Forces (eV/Å)\t{mad_forces:.4f}\n")

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage: python script.py <trajectory_file.xyz>")
    sys.exit(1)

  filename = sys.argv[1]
  analyze_trajectory(filename)