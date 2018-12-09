class Cell:
    def __init__(self, number):
        self.number = number
        self.value = None

    def getid(self):
        return self.number[2:]

    def setvalue(self, value):
        """Values are passed as a string representation of a hex value
        or as a hex value. They are not passed as ints."""
        self.value = int(value, 16)

    def getvalue(self):
        """Values returned are base 16 int."""
        if self.value is not None:
            return self.value

    def tostr(self):
        if self.value is None:
            return "__"
        else:
            return str(hex(self.value))[2:]
