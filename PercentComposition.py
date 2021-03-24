from ChemicalElements import periodic_table
from Compound import Compound
from MolarMass import MolarMass


class PercentComposition:
    """
    Inputting a compound itself will return the percent composition of each element.
    Inputting a percent composition of a compound's elements will return the original compound (symbol: percentage)
    (Percentage in decimals)
    """
    def __init__(self, compound=None, **kwargs):
        self.__elements = periodic_table
        self.__compound = compound
        self.__percentages = kwargs
        if compound is not None:
            self.__molarMass = MolarMass(compound)

    def elementPercentagesCalc(self):
        composition = {}
        if self.__compound is not None:
            elements = Compound(self.__compound)
            for element in elements:
                symbol = element
                coefficient = elements[symbol]

                if coefficient is not None:
                    composition[symbol] = round(periodic_table[symbol]["atomic_mass"] * coefficient / float(self.__molarMass), 4)
                else:
                    composition[symbol] = round(periodic_table[symbol]["atomic_mass"] / float(self.__molarMass), 4)

            return composition

        return None

    def findCompound(self):
        molecule = {}
        smallestMol = None
        fractions = [0, 1/3, 0.25, 2/3, 0.5, 0.75, 1]
        for symbol, percentage in self.__percentages.items():
            molecule[symbol] = percentage * 100 / periodic_table[symbol]["atomic_mass"]  # find the number of moles
            if smallestMol is None:
                smallestMol = molecule[symbol]
            else:
                if molecule[symbol] < smallestMol:
                    smallestMol = molecule[symbol]

        molecule = {symbol: round(mole / smallestMol, 1) for symbol, mole in molecule.items()}

        def mole_multiplier(molecules: dict):
            multiplier = 1
            for element, molecule in molecules.items():
                molecule = float(str(molecule)[1:])
                closest_fraction = self.closest(fractions, molecule)
                if closest_fraction == 0:
                    continue
                elif closest_fraction == 1/3 or closest_fraction == 2/3:
                    multiplier *= 3
                elif closest_fraction == 0.25 or closest_fraction == 0.75:
                    multiplier *= 4
                elif closest_fraction == 0.5:
                    multiplier *= 2
                elif closest_fraction == 1:
                    multiplier *= 1
            return multiplier

        multiplier = mole_multiplier(molecule)

        molecule = {symbol: round(mole * multiplier) for symbol, mole in molecule.items()}
        return molecule

    @staticmethod
    def closest(fractions, mole_value):
        return fractions[min(range(len(fractions)), key=lambda i: abs(fractions[i] - mole_value))]


if __name__ == '__main__':
    percentComp = PercentComposition(c=0.2, h=0.3, n=0.5)
    print(percentComp.elementPercentagesCalc())
    percentComp.findCompound()
