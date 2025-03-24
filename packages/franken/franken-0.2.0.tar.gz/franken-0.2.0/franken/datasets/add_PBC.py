import ase.io
from ase import Atoms
import numpy as np
import argparse

def create_periodic_cell_for_trajectory(trajectory_file, output_file, padding=100.0):
    # Load all frames from the trajectory file
    trajectory = ase.io.read(trajectory_file, index=':')  # Read all frames

    # Create a list to store frames with periodic cells
    frames_with_cells = []

    # Loop over each frame in the trajectory
    for atoms in trajectory:
        # Get the positions of all atoms in the structure
        positions = atoms.get_positions()

        # Find the minimum and maximum coordinates in each direction (x, y, z)
        min_pos = np.min(positions, axis=0)
        max_pos = np.max(positions, axis=0)

        # Calculate the size of the box needed to enclose the molecule with padding
        cell_lengths = max_pos - min_pos + 2 * padding

        # Set the periodic cell with the calculated size
        atoms.set_cell(cell_lengths)
        atoms.center()  # Center the atoms inside the cell

        # Enable periodic boundary conditions
        atoms.set_pbc(True)

        # Append the modified frame to the list
        frames_with_cells.append(atoms)

    # Write all frames with periodic cells to a new trajectory file
    ase.io.write(output_file, frames_with_cells)

def main():
    parser = argparse.ArgumentParser(description="A script for adding PBC to each frame of a given trajectory in order to be used as a periodic system (fairchem requires this). Provide the original trajecotry name, a suffix for the new trajectory and the amount of padding.")

    # Mandatory argument
    parser.add_argument("original_traj", type=str, help="Original trajectory to add PBC to")

    # Optional arguments
    parser.add_argument("--newtraj_suffix", type=str, default="_pbc.xyz", help="Resulting filename, by default just adds '_pbc' suffix to the original trajectory name")
    parser.add_argument("--padding", type=float, default=100.00, help="Padding size for the PBC to be added. Use a big number to ensure images don't see each other for non-periodic systems.")
    args = parser.parse_args()

    newtraj = args.original_traj.split(".")[0] + args.newtraj_suffix
    
    # Accessing the arguments
    print("Original traj:", args.original_traj)
    print("Resulting traj:", newtraj)
    print("Size of padding (Ang):", args.padding)

    # Example usage:
    # Replace 'input.traj' with your actual trajectory file, and 'output.traj' with the desired output file
    # We can do it directly with the previous produced splits. 
    create_periodic_cell_for_trajectory(args.original_traj,newtraj, padding=args.padding)

if __name__ == "__main__":
    main()