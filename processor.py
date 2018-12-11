class Cell:
    def __init__(self, number):
        self.number = number
        self.value = None

    def getid(self):
        return self.number[2:]

    def setvalue(self, value):
        """Sets the contents of the cell.
        (The value must be passed as a hexadecimal value or as a string
        representation of a hexadecimal value.

        Args:
            value (str): a hex representation of the contents of the cell

        """
        self.value = int(value, 16)


    def getvalue(self):
        """Returns the contents of the cell as an integer.

        Returns:
            int: an integer representation of the cell's contents

        """
        if self.value is not None:
            return self.value

    def tostr(self):
        if self.value is None:
            return "00"
        else:
            return str(hex(self.value))[2:].zfill(2)
