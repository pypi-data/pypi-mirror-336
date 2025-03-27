import re
import argparse
from ase.io import read


def parse_configuration(data):
    # Parse sections using regular expressions
    num_atoms = int(re.search(r"The number of atoms\s*[-=]+\s*(\d+)", data).group(1))
    energy = float(
        re.search(r"Total energy \(eV\)\s*[-=]+\s*([-+]?\d*\.\d+|\d+)", data).group(1)
    )

    # Extract lattice vectors
    lattice_match = re.search(
        r"Primitive lattice vectors \(ang.\)\s*[-=]+\s*([\d\s.-]+)", data
    )
    lattice_lines = lattice_match.group(1).strip().split("\n")
    lattice = [line.split() for line in lattice_lines]

    # Flatten and format lattice as a string for XYZ format
    lattice_flat = " ".join([" ".join(line) for line in lattice])

    # Extract atomic positions
    positions_match = re.search(
        r"Atomic positions \(ang.\)\s*[-=]+\s*([\d\s.-]+)", data
    )
    positions_lines = positions_match.group(1).strip().split("\n")
    positions = [line.split() for line in positions_lines]

    # Extract forces
    forces_match = re.search(r"Forces \(eV ang.\^-1\)\s*[-=]+\s*([\d\s.-]+)", data)
    forces_lines = forces_match.group(1).strip().split("\n")
    forces = [line.split() for line in forces_lines]

    # Extract stress tensor (two lines) without separators
    stress_match_1 = re.search(
        r"Stress \(kbar\)\s*[-=]+\s*XX YY ZZ\s*[-=]+\s*([\d\s.-]+)", data
    )
    stress_match_2 = re.search(r"XY YZ ZX\s*[-=]+\s*([\d\s.-]+)", data)

    # Ensure we only capture numerical values and not separator lines
    stress_values_1 = (
        stress_match_1.group(1).strip().split()[:3]
    )  # Take first three values for XX YY ZZ
    stress_values_2 = (
        stress_match_2.group(1).strip().split()[:3]
    )  # Take first three values for XY YZ ZX
    xx, yy, zz = stress_values_1
    xy, yz, zx = stress_values_2

    # Combine the two stress components into a single list
    # stress_tensor = stress_values_1 + stress_values_2
    # stress_tensor = ' '.join(stress_tensor)  # Convert to a single string
    stress_tensor = f"{xx} {xy} {zx} {xy} {yy} {yz} {zx} {yz} {zz}"

    # Create the extended XYZ content for this configuration
    xyz_content = []
    xyz_content.append(f"{num_atoms}")
    xyz_content.append(
        f'Lattice="{lattice_flat}" Properties=species:S:1:pos:R:3:forces:R:3 energy={energy} stress="{stress_tensor}"'
    )

    # Atom types (order them according to the positions provided)
    atom_type_lines = (
        re.search(r"Atom types and atom numbers\s*[-=]+\s*([\w\s\d]+)", data)
        .group(1)
        .strip()
        .split("\n")
    )
    atom_types = []
    for line in atom_type_lines:
        element, count = line.split()
        atom_types.extend([element] * int(count))

    # Add each atom's data line by line
    for idx, (position, force) in enumerate(zip(positions, forces)):
        element = atom_types[idx]
        px, py, pz = position
        fx, fy, fz = force
        xyz_content.append(f"{element} {px} {py} {pz} {fx} {fy} {fz}")

    return "\n".join(xyz_content)


def parse_multiple_configurations(data):
    # Split the data by configurations using "Configuration num." as the delimiter
    configurations = re.split(r"Configuration num\.\s*\d+", data)
    xyz_all = []

    # Process each configuration if it is not empty
    for config in configurations:
        config = config.strip()
        if config:  # Only parse if the configuration is not empty
            try:
                xyz_all.append(parse_configuration(config))
            except Exception as e:
                print(f"Error parsing configuration: {e}")

    # Join all configurations with a newline
    return "\n".join(xyz_all)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MLFF to xyz converter")
    parser.add_argument("-f", "--filename", help="Input Filename")
    args = parser.parse_args()

    filename = args.filename

    print(f"Conversion input: {filename}")

    with open(filename, "r") as file:
        data = file.read()

    xyz_output = parse_multiple_configurations(data)

    with open(filename + ".xyz", "w") as file:
        file.write(xyz_output)

    print(f"Output written to {filename}.xyz")

    traj = read(filename + ".xyz", index=":")
    print(f"Dataset has {len(traj)} frames")
    for i, atoms in enumerate(traj):
        atoms.get_potential_energy()
        atoms.get_forces()

    print("End of conversion")
