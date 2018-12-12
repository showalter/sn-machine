class Cell:
    """an encapsulation of a memory cell or register

    Attributes:
        id (int): the number of the cell
        value (int): the contents of the cell

    """


    def __init__(self, number):
        """Constructs and intializes the id and value for a cell

        """
        self.number = number
        self.value = None


    def getid(self):
        """Returns the string representation of the ID

    """
        return self.number[2:]


    def setvalue(self, value):
        """Sets the contents of the cell.

        The value must be passed as a hexadecimal value or as a string
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
        """Returns the a string reorientation of the contents of the cell.

        """

        if self.value is None:
            return "00"
        else:
            return str(hex(self.value))[2:].zfill(2)
