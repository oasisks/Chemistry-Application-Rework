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


def test(verbose=True):
    assert periodic_table['H'] == {'name': 'Hydrogen', 'atomic_mass': 1.008, 'boil': 20.271, 'category': 'diatomic nonmetal', 'color': None, 'density': 0.08988, 'melt': 13.99, 'molar_heat': 28.836, 'number': 1, 'period': 1, 'phase': 'Gas', 'spectral_img': 'https://en.wikipedia.org/wiki/File:Hydrogen_Spectra.jpg', 'symbol': 'H', 'xpos': 1, 'ypos': 1, 'shells': [1], 'electron_configuration': '1s1', 'electron_configuration_semantic': '1s1', 'electron_affinity': 72.769, 'electronegativity_pauling': 2.2, 'ionization_energies': [1312]}
    assert periodic_table['U'] == {'name': 'Uranium', 'atomic_mass': 238.028913, 'boil': 4404, 'category': 'actinide', 'color': None, 'density': 19.1, 'melt': 1405.3, 'molar_heat': 27.665, 'number': 92, 'period': 7, 'phase': 'Solid', 'spectral_img': None, 'symbol': 'U', 'xpos': 6, 'ypos': 10, 'shells': [2, 8, 18, 32, 21, 9, 2], 'electron_configuration': '1s2 2s2 2p6 3s2 3p6 4s2 3d10 4p6 5s2 4d10 5p6 6s2 4f14 5d10 6p6 7s2 5f3 6d1', 'electron_configuration_semantic': '[Rn] 5f3 6d1 7s2', 'electron_affinity': 50.94, 'electronegativity_pauling': 1.38, 'ionization_energies': [597.6, 1420]}
    if verbose:
        print("All tests passed for Chemical Elements.")


if __name__ == "__main__":
    test()
