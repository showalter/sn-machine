class Cell:
    def __init__(self, number):
        self.number = number
        self.value = None

    def getid(self):
        return self.number[2:]

    def setvalue(self, value):
        self.value = value

    def getvalue(self):
        if self.value is None:
            return "__"
        else:
            return str(self.value)
