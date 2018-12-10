class Cell:
    def __init__(self, number):
        self.number = number
        self.value = None

    def getid(self):
        return self.number[2:]

    def setvalue(self, value):
        """Values must be passed as a string representation of a hex value
        or as a hex value. They should not be passed as ints

        Args:
            value (str): a hex representation of the contents of the cell

        """
        self.value = int(value, 16)


    def getvalue(self):
        """Values will be returned as base 16 int.

        Return:
            int: an integer representation of the cells contents

        """
        if self.value is not None:
            return self.value

    def tostr(self):
        if self.value is None:
            return "00"
        else:
            return str(hex(self.value))[2:].zfill(2)
