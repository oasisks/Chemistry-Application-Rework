from ChemicalElements import periodic_table
from Compound import Compound


class MolarMass:
    """
    Calculates the molar mass of a given compound. Should be able to separate compounds (Assuming the equation itself
    is not bogus)

    Cast string for formula.
    Cast float for the molar
    Note: Kg gives less significant digits than g
    """
    def __init__(self, compound: str, kg=False):
        """
        :param compound: the chemical molecule (assuming the compound was syntax correctly)
        :param kg: Bool. Determines whether the values would be in grams or kilograms
        """
        self.__elements = periodic_table
        self.__compound = Compound(compound)
        self.__kg = kg
        self.__molarMass = self._calculateMass()

    def __str__(self):
        return "".join([f"{symbol}{amount}" for symbol, amount in self.__compound.items()])

    def __float__(self):
        return self.__molarMass

    def _calculateMass(self):
        """
        calculates the molar mass in g/kg
        :return: float
        """
        mass = 0
        print(self.__compound)
        for component in self.__compound:
            element = component
            number = self.__compound[component]

            # if its empty
            mass += periodic_table[element]["atomic_mass"] * number

        if self.__kg:
            return round(mass / 1000, 3)

        return round(mass, 3)


if __name__ == '__main__':
    molarMass = MolarMass("C6H12O6", kg=False)
    print(molarMass)
    print(float(molarMass))
