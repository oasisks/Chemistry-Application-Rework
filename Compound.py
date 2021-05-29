from re import findall, split, compile, search
from ChemicalElements import periodic_table

_nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

_subscript = {1: "\u2081", 2: "\u2082", 3: "\u2083", 4: "\u2084", 5: "\u2085", 6: "\u2086", 7: "\u2087",
              8: "\u2088", 9: "\u2089"}


class Compound(dict):
    """
    Formula
    """
    def __init__(self, formula, /, charge=None):
        dict.__init__(self)

        if charge is not None:
            self.charge = charge
        else:
            self.charge = 0

        if type(formula) == str:
            constitutents = findall(r"[A-Z][a-z]*[0-9]*", formula)
            charge = findall(r"[−\-+][0-9]*", formula)
            for constituent in constitutents:
                found = split(r"(?<=[a-zA-Z])(?=[0-9])", constituent)
                if len(found) == 1:
                    if constituent not in self:
                        self[constituent] = 1
                    else:
                        self[constituent] += 1
                else:
                    symbol, amount = found
                    if symbol not in self:
                        self[symbol] = int(amount)
                    else:
                        self[symbol] += int(amount)
            if charge:
                charge = charge[0]
                if len(charge) > 1:
                    if charge[0] == "−" or charge[0] == "-":
                        self.charge = int(charge[1:]) * -1
                    else:
                        self.charge = int(charge[1:])
                else:
                    if charge[0] == "−" or charge[0] == "-":
                        self.charge = -1
                    else:
                        self.charge = 1

        elif type(formula) == dict:
            for key in formula:
                self[key] = formula[key]

    def __eq__(self, other):
        if type(other) == Compound:
            if dict.__eq__(self, other) and self.charge == other.charge:
                return True
            else:
                return False
        else:
            return dict.__eq__(self, other)

    def __str__(self):
        formula = ""
        for symbol, coefficient in self.items():
            if coefficient == 1:
                formula += f"{symbol}"
                continue
            formula += f"{symbol}{_subscript[coefficient]}"


        return formula

    def molarMass(self, kg=False):
        mass = 0
        for symbol, quantity in self.items():
            mass += periodic_table[symbol]["atomic_mass"] * quantity

        if kg:
            return mass / 1000

        return mass

    def percentComposition(self) -> dict:
        composition = {}
        compoundMass = self.molarMass()
        for symbol, quantity in self.items():
            composition[symbol] = periodic_table[symbol]["atomic_mass"] / compoundMass

        return composition

    @staticmethod
    def isMalformed(equation: str):
        equation = [[y.strip() for y in x.strip().split("+")] for x in split(r"->|=", equation)]
        validChar = True
        for row in equation:
            for col in row:
                for character in col:
                    asciiVal = ord(character)
                    if 48 <= asciiVal <= 57 or 65 <= asciiVal <= 90 or 97 <= asciiVal <= 122:
                        continue

                    # if at least one of the inputted compound does not have contain valid characters
                    validChar = False

        if validChar:
            for row in equation:
                for col in row:
                    constituents = findall(r"[A-Z][a-z]*[0-9]*", col)
                    if len(col) != len("".join(constituents)):
                        # something is wrong with one or more of the expression
                        return True

                    # check if the constituent parts are within the periodic table
                    # print(constituents)
                    for constituent in constituents:
                        element = split(r"(?<=[a-zA-Z])(?=[0-9])", constituent)[0]
                        if element not in periodic_table:
                            return True
                        print(element)

            return False

        return True


def test(verbose=True):
    assert Compound("C6H12O6") == Compound({'C': 6, 'H': 12, 'O': 6}, charge=0)
    assert Compound("HCOF") == Compound({'H': 1, 'C': 1, 'O': 1, 'F': 1}, charge=0)
    assert Compound("2NH3OH+") == Compound({"N": 1, "H": 4, "O": 1}, charge=1)
    assert Compound("2NH3O2H2-2") == Compound({"N": 1, "H": 5, "O": 2}, charge=-2)
    if verbose:
        print("All tests passed for Compound")


if __name__ == "__main__":
    test()
    compound = Compound("H2O")
    mass = compound.molarMass(kg=True)
    composition = compound.percentComposition()
    print(compound)
    print(mass)
    print(composition)
    print(Compound.isMalformed("H2O"))

