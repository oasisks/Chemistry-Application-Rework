import json
import re


class Elements:
    def __init__(self):
        # initializing the elements class
        self.__fileName = "PeriodicTableJSON.json"
        self.__file = open(self.__fileName, "r", encoding="utf-8")
        self.__rawElements = json.load(self.__file)["elements"]
        self.__elements = {}
        self.__nameSymbolPair = {}
        self.__symbolNamePair = {}
        for element in self.__rawElements:
            key = (element["name"].lower(), element["symbol"].lower())
            value = {tag: info for tag, info in element.items() if tag not in ["name", "symbol"]}
            # print(key, value)
            self.__elements[key] = value
            self.__nameSymbolPair[key[0]] = key[1]
            self.__symbolNamePair[key[1]] = key[0]

    def _getKey(self, name) -> "(name, symbol)":
        """
        returns a key of the elements dictionary
        :param name: str (symbol or name)
        :return: ()
        """
        name = name.lower()
        if name in self.__nameSymbolPair:
            return name, self.__nameSymbolPair[name]
        elif name in self.__symbolNamePair:
            return self.__symbolNamePair[name], name

        return None

    def getMass(self, name: str):
        """
        returns the mass in grams
        :param name: str
        :return: float
        """
        if self._getKey(name) is not None:
            return self.__elements[self._getKey(name)]["atomic_mass"]

        return None

    def getDensity(self, name: str):
        """
        returns the density in grams per mL or cm^3
        :param name: str
        :return: float
        """
        if self._getKey(name) is not None:
            return self.__elements[self._getKey(name)]["density"]

        return None

    def getElectronConfiguration(self, name: "can be the name or symbol"):
        """
        returns a string containing the entire electron configuration
        :param name: str
        :return: str
        """
        if self._getKey(name) is not None:
            return self.__elements[self._getKey(name)]["electron_configuration"]

        return None

    def getNobelGasConfiguration(self, name: "can be the name or symbol"):
        """
        returns a string containing the nobel gas electron configuration
        :param name: str
        :return: str
        """
        if self._getKey(name) is not None:
            return self.__elements[self._getKey(name)]["electron_configuration_semantic"]

        return None

    def electronAffinity(self, name: "can be the name or symbol"):
        """
        returns the electron affinity
        :param name: str
        :return: float
        """
        if self._getKey(name) is not None:
            return self.__elements[self._getKey(name)]["electron_affinity"]

        return None

    def getIonizationEnergy(self, name: "can be the name or symbol"):
        """
        returns the ionization energy for each element (in kJ per mole)
        :param name: str
        :return: []
        """
        if self._getKey(name) is not None:
            return self.__elements[self._getKey(name)]["ionization_energies"]

        return None

    @staticmethod
    def findAllConstituentElement(compound):
        return re.findall("[A-Z][a-z]?\d*|\(.*?\)\d+", compound)

    @staticmethod
    def findElementSymbol(element):
        """
        Returns the symbol of the element (i.e. H2 - > H)
        :param element: str
        :return: str
        """
        return re.findall("[a-zA-z]", element)[0]

    @staticmethod
    def findCoefficientOfElement(element):
        """
        Returns the coefficient of an element (if there is coefficient)
        :param element:
        :return:
        """
        coefficient = re.findall("[0-9]", element)

        # if there are coefficients
        if coefficient:
            return int(coefficient[0])

        return None
