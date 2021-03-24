from re import findall, split

_nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


class Compound(dict):
    def __init__(self, formula):
        dict.__init__(self)
        constitutents = findall(r"[A-Z][a-z]*[0-9]*", formula)
        for constituent in constitutents:
            found = split(r"(?<=[a-zA-Z])(?=[0-9])", constituent)
            if len(found) == 1:
                self[constituent] = 1
            else:
                symbol, amount = found
                self[symbol] = int(amount)
