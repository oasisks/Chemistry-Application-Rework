from ChemicalElements import Elements


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
        self.__elements = Elements()
        self.__compound = self.__elements.findAllConstituentElement(compound)
        self.__kg = kg
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
            element = self.__elements.findElementSymbol(component)
            number = self.__elements.findCoefficientOfElement(component)

            # if its empty
            if number is None:
                # there is only 1 element
                mass += self.__elements.getMass(element)
            else:
                mass += self.__elements.getMass(element) * number

        if self.__kg:
            return round(mass / 1000, 3)

        return round(mass, 3)


if __name__ == '__main__':
    molarMass = MolarMass("C6H12O6", kg=False)
    print(molarMass)
    print(float(molarMass))
