import re
from ChemicalElements import Elements


class MolarMass:
    """
    Calculates the molar mass of a given compound. Should be able to separate compounds (Assuming the equation itself
    is not bogus)

    Cast string for formula.
    Cast float for the molar
    """
    def __init__(self, compound: str, kg=False):
        """
        :param compound: the chemical molecule (assuming the compound was syntax correctly)
        :param kg: Bool. Determines whether the values would be in grams or kilograms
        """
        self.__compound = re.findall("[A-Z][a-z]?\d*|\(.*?\)\d+", compound)
        self.__kg = kg
        self.__elements = Elements()
        self.__molarMass = self._calculateMass()

    def __str__(self):
        return "".join(self.__compound)

    def __float__(self):
        return self.__molarMass

    def _calculateMass(self):
        """
        calculates the molar mass in g/kg
        :return: float
        """
        mass = 0
        for component in self.__compound:
            element = re.findall("[a-zA-z]", component)[0]
            number = re.findall("[0-9]", component)

            # if its empty
            if not number:
                # there is only 1 element
                mass += self.__elements.getMass(element)
            else:
                mass += self.__elements.getMass(element) * int(number[0])

        if self.__kg:
            return mass / 1000

        return mass


if __name__ == '__main__':
    molarMass = MolarMass("H2SO4")
    print(molarMass)
    print(float(molarMass))
