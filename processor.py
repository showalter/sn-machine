"""
The processor module contains the Cell class

Copyright (c) Ryan Showalter and Cole Nutter under the terms of the MIT License
"""


class Cell:
    """an encapsulation of a memory cell or register

    Attributes:
        __number (int): the number of the cell
        __value (int): the contents of the cell
    """

    def __init__(self, number):
        """ Construct and initialize the id and value of a cell"""

        self.__number = number
        self.__value = None

    def getid(self):
        """ Return a string representation of a cell's id"""

        return self.__number[2:]

    def setvalue(self, value):
        """ Set the contents of a cell

        The value must be passed as a hexadecimal value or as a string
        representation of a hexadecimal value.

        Args:
            value (str): a hex representation of the contents of the cell
        """

        self.__value = int(value, 16)

    def getvalue(self):
        """ Return the contents of a cell as an integer

        Returns:
            int: an integer representation of the cell's contents
        """

        if self.__value is not None:
            return self.__value
        else:
            return 0

    def tostr(self):
        """ Return a string representation of the contents of the cell"""

        if self.__value is None:
            return "00"
        else:
            return str(hex(self.__value))[2:].zfill(2)
