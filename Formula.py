from ChemicalElements import periodic_table
from Compound import Compound


class Formula(dict):
    def __init__(self, mass=0, **kwargs):
        dict.__init__(self)
        self.update(kwargs)
        self.availableMass = mass

    def empiricalFormula(self) -> dict:
        formula = {}
        smallestMol = None

        fractions = [0, 1/3, 0.25, 2/3, 0.5, 0.75, 1]

        for symbol, percentAbundance in self.items():
            formula[symbol] = percentAbundance * 100 / periodic_table[symbol]["atomic_mass"]  # num of moles
            if smallestMol is None:
                smallestMol = formula[symbol]
            else:
                if formula[symbol] < smallestMol:
                    smallestMol = formula[symbol]

        formula = {symbol: round(mole / smallestMol, 1) for symbol, mole in formula.items()}

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

        multiplier = mole_multiplier(formula)

        formula = {symbol: round(mole * multiplier) for symbol, mole in formula.items()}
        return formula

    @staticmethod
    def closest(fractions, mole_value):
        return fractions[min(range(len(fractions)), key=lambda i: abs(fractions[i] - mole_value))]

    def molecularFormula(self):
        empiricalFormula = self.empiricalFormula()
        compound = Compound(empiricalFormula)
        if self.availableMass == 0:
            return "No Mass Inputted"

        multiplier = self.availableMass / compound.molarMass()

        molecularFormula = {symbol: quantity * multiplier for symbol, quantity in empiricalFormula.items()}

        return molecularFormula


if __name__ == '__main__':
    formula = Formula(C=0.2, H=0.3, N=0.5, mass=321)
    print(formula.empiricalFormula())
    print(formula.molecularFormula())
