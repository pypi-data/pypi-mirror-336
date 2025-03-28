from typing import Literal


elements = [
    "Ag",
    "Au",
    "Cd",
    "Co",
    "Cr",
    "Cu",
    "Fe",
    "Hf",
    "Hg",
    "Ir",
    "Mn",
    "Mo",
    "Nb",
    "Ni",
    "Os",
    "Pd",
    "Pt",
    "Re",
    "Rh",
    "Ru",
    "Ta",
    "Tc",
    "Ti",
    "V",
    "W",
    "Zn",
    "Zr",
]
MELTING_POINTS = {
    "Ag": 1235,
    "Au": 1337,
    "Cd": 594,
    "Co": 1768,
    "Cr": 2180,
    "Cu": 1358,
    "Fe": 1811,
    "Hf": 2506,
    "Hg": 234,
    "Ir": 2739,
    "Mn": 1519,
    "Mo": 2896,
    "Nb": 2750,
    "Ni": 1728,
    "Os": 3306,
    "Pd": 1828,
    "Pt": 2041,
    "Re": 3459,
    "Rh": 2237,
    "Ru": 2607,
    "Ta": 3290,
    "Tc": 2430,
    "Ti": 1941,
    "V": 2183,
    "W": 3695,
    "Zn": 693,
    "Zr": 2128,
}
TEMPERATURE_LABELS = ["cold", "warm", "melt"]
TEMPERATURE_MULTIPLIERS = {
    "cold": 0.25,
    "warm": 0.75,
    "melt": 1.25,
}


def tm23_temp(
    element: str, temperature_label: Literal["cold", "warm", "melt"]
) -> float:
    if temperature_label not in TEMPERATURE_LABELS:
        raise ValueError(
            f"'temperature_label' must be one of {TEMPERATURE_LABELS} "
            f"but found '{temperature_label}'."
        )
    if element not in elements:
        raise ValueError(f"Element '{element}' is not a valid TM23 element label.")
    melt_point = MELTING_POINTS[element]
    sim_temp = melt_point * TEMPERATURE_MULTIPLIERS[temperature_label]
    return sim_temp
