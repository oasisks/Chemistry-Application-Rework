import re
import numpy as np
from ChemicalElements import periodic_table
from Compound import Compound


class EquationBalancer:
    """
    Balances a chemical equation in a specific format (i.e O2 + H2 -> H20)
    """

    def __init__(self, unBalancedEquation: str):
        self.__unBalancedEquation = unBalancedEquation
        self.__elements = periodic_table

    def __str__(self):
        return self._findBalancedEquation(self.__unBalancedEquation)

    def _findBalancedEquation(self, unBalancedEquation):
        balancedEquation = ""
        rawEquation = [[compound.strip() for compound in re.split(r"\+", side.strip())]
                       for side in re.split("->|=", unBalancedEquation)]
        realSolution = True

        reactants = rawEquation[0]
        products = rawEquation[1]

        availableElements = self.availableElements(reactants, products)
        matrixA = []
        vectorB = []
        # Initialize the matrix and vector
        for availableElement in availableElements:
            matrixEntry = []
            vectorEntry = []

            for index in range(len(reactants)):
                exists = False
                compound = Compound(reactants[index])
                for constituentPart in compound:
                    if availableElement == constituentPart:
                        exists = True
                        coefficient = compound[constituentPart]
                        matrixEntry.append(coefficient)
                if not exists:
                    matrixEntry.append(0)

            for index in range(len(products)):
                exists = False
                compound = Compound(products[index])
                constituentParts = compound.keys()
                # last entry
                if len(products) - 1 == index:
                    for constituentPart in constituentParts:
                        if availableElement == constituentPart:
                            exists = True
                            coefficient = compound[constituentPart]
                            vectorEntry.append(coefficient)
                    if not exists:
                        vectorEntry.append(0)
                else:
                    for constituentPart in constituentParts:
                        if availableElement == constituentPart:
                            exists = True
                            coefficient = compound[constituentPart]
                            matrixEntry.append(-coefficient)
                            # matrixEntry.append(-coefficient)
                    if not exists:
                        matrixEntry.append(0)

            matrixA.append(matrixEntry)
            vectorB.append(vectorEntry)

        matrixA = np.array(matrixA)
        vectorB = np.array(vectorB)

        linearRegression = np.linalg.lstsq(matrixA, vectorB, rcond=None)
        solution = linearRegression[0]
        residual = linearRegression[1]

        # if there are residuals
        if residual.size > 0:
            # this equation most likely does not exist in real life and probably has no real solution
            realSolution = False

        if realSolution:
            determinantOfA = np.linalg.det(matrixA)
            solution *= determinantOfA
            gcd = np.gcd.reduce(solution.astype(np.int64))
            solution /= gcd
            solution = solution.astype(np.int64)

            for index, reactant in enumerate(reactants):
                coefficient = abs(solution[index])
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
                    coefficient = abs(solution[index])
                    if coefficient == 1:
                        balancedEquation += f" {product} + "
                    else:
                        balancedEquation += f" {coefficient}{product} + "
        else:
            balancedEquation = f"No Real Solution for {self.__unBalancedEquation}"
        return balancedEquation

    def availableElements(self, reactants, products):
        availableElements = []
        compounds = reactants + products

        for compound in compounds:
            compound = Compound(compound)
            for part in compound:
                if part not in availableElements:
                    availableElements.append(part)

        return availableElements


if __name__ == '__main__':
    balancer = EquationBalancer("O2 -> H2O")
    print(balancer)
