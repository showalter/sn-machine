class Cell:
    def __init__(self, number):
        self.number = number
        self.value = None

    def getid(self):
        return self.number[2:]

    # Values must be passed as a string representation of a hex
    # value, or as a hex value. They should not be passed as ints.
    def setvalue(self, value):
        self.value = int(value, 16)

    # Values will be returned as a base 16 int.
    def getvalue(self):
        if self.value is not None:
            return self.value

    def tostr(self):
        if self.value is None:
            return "__"
        else:
            return str(hex(self.value))[2:]
