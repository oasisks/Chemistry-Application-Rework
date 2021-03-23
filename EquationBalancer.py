import re
import numpy as np
from ChemicalElements import Elements


class EquationBalancer:
    """
    Balances a chemical equation in a specific format (i.e O2 + H2 -> H20)
    """

    def __init__(self, unBalancedEquation: str):
        self.__unBalancedEquation = unBalancedEquation
        self.__elements = Elements()

    def __str__(self):
        return self._findBalancedEquation(self.__unBalancedEquation)

    def _findBalancedEquation(self, unBalancedEquation):
        balancedEquation = ""
        rawEquation = [[compound.strip() for compound in re.split(r"\+", side.strip())]
                       for side in re.split("->|=", unBalancedEquation)]

        reactants = rawEquation[0]
        products = rawEquation[1]

        availableElements = self.availableElements(reactants, products)
        matrixA = []
        vectorB = []
        print(availableElements)
        for availableElement in availableElements:
            matrixEntry = []
            vectorEntry = []

            for index in range(len(reactants)):
                exists = False
                constituentParts = self.__elements.findAllConstituentElement(reactants[index])
                for constituentPart in constituentParts:
                    if availableElement in constituentPart:
                        exists = True
                        coefficient = self.__elements.findCoefficientOfElement(constituentPart)
                        if coefficient is not None:
                            matrixEntry.append(coefficient)
                        else:
                            matrixEntry.append(1)
                if not exists:
                    matrixEntry.append(0)

            for index in range(len(products)):
                exists = False
                constituentParts = self.__elements.findAllConstituentElement(products[index])
                # last entry
                if len(products) - 1 == index:
                    for constituentPart in constituentParts:
                        if availableElement in constituentPart:
                            exists = True
                            coefficient = self.__elements.findCoefficientOfElement(constituentPart)
                            if coefficient is not None:
                                vectorEntry.append(coefficient)
                            else:
                                vectorEntry.append(1)
                    if not exists:
                        vectorEntry.append(0)
                else:
                    for constituentPart in constituentParts:
                        if availableElement in constituentPart:
                            exists = True
                            coefficient = self.__elements.findCoefficientOfElement(constituentPart)
                            if coefficient is not None:
                                matrixEntry.append(-coefficient)
                            else:
                                matrixEntry.append(-1)
                            # matrixEntry.append(-coefficient)
                    if not exists:
                        matrixEntry.append(0)

            matrixA.append(matrixEntry)
            vectorB.append(vectorEntry)

        matrixA = np.array(matrixA)
        vectorB = np.array(vectorB)
        print(matrixA)
        print(vectorB)
        inverseMatrixA = np.linalg.inv(matrixA)
        determinantOfA = np.linalg.det(matrixA)

        coefficients = np.matmul(inverseMatrixA, vectorB) * determinantOfA
        coefficients = np.reshape(coefficients, coefficients.size).astype(np.int64)
        gcd = np.gcd.reduce(coefficients)
        coefficients = (coefficients / gcd).astype(np.int64)
        for index, reactant in enumerate(reactants):
            coefficient = abs(coefficients[index])
            if index == len(reactants) - 1:
                if coefficient == 1:
                    balancedEquation += f"{reactant} ->"
                else:
                    balancedEquation += f"{coefficient}{reactant} ->"
            else:
                if coefficient == 1:
                    balancedEquation += f"{reactant} + "
                else:
                    balancedEquation += f"{coefficient}{reactant} + "

        for index, product in enumerate(products):
            index += len(reactants)
            if index >= len(product) - 1:
                coefficient = abs(int(determinantOfA / gcd))
                if coefficient == 1:
                    balancedEquation += f" {product}"
                else:
                    balancedEquation += f" {coefficient}{product}"
            else:
                coefficient = abs(coefficients[index])
                if coefficient == 1:
                    balancedEquation += f" {product} + "
                else:
                    balancedEquation += f" {coefficient}{product} + "
        return balancedEquation

    def availableElements(self, reactants, products):
        availableElements = []
        elements = reactants + products

        for element in elements:
            constituentParts = self.__elements.findAllElementSymbol(element)
            for part in constituentParts:
                if part not in availableElements:
                    availableElements.append(part)

        return availableElements


if __name__ == '__main__':
    balancer = EquationBalancer("C6H12O6 -> H2O + C2")
    print(balancer)
