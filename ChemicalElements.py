from json import load
from typing import TypedDict, Union, List, Dict


class Element(TypedDict):
    name: str
    symbol: str
    atomic_mass: float
    boil: float
    category: str
    color: Union[str, type(None)]
    density: float
    melt: float
    molar_heat: float
    number: int
    period: int
    phase: str
    spectral_img: str
    xpos: int
    ypos: int
    shells: List[int]
    electron_configuration: str
    electron_configuration_semantic: str
    electron_affinity: float
    electronegativity_pauling: float
    ionization_energies: List[float]


periodic_table: Dict[str, Element] = {}

__fileName = "PeriodicTableJSON.json"
__file = open(__fileName, "r", encoding="utf-8")
__rawElements = load(__file)["elements"]
for element in __rawElements:
    key = element["symbol"]
    value: Element = {tag: info for tag, info in element.items() if tag in Element.__annotations__}
    periodic_table[key] = value

if __name__ == "__main__":
    print(periodic_table['H'])
