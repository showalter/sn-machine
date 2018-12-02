from processor import Cell

cells = []
registers = []

icounter = None

complete = False

__instructions = \
    {'1': 'load_from_cell', '2': 'load_with',
     '3': 'store', '4': 'move',
     '5': 'add_complement', '6': 'add_float',
     '7': 'or', '8': 'and',
     '9': 'xor', 'a': 'rotate',
     'b': 'jump', 'c': 'halt'}


def execute_instruction(a, b):
    global icounter
    instruction = create_instruction(a.getvalue(), b.getvalue())
    opcode = instruction[0]
    operation = __instructions[opcode]
    icounter = icounter + 2

    if opcode == '1':
        load_from_cell(instruction)
    elif opcode == '2':
        load_with(instruction)
    elif opcode == '3':
        store(instruction)
    elif opcode == '4':
        move(instruction)
    elif opcode == '5':
        add_complement(instruction)
    elif opcode == '6':
        add_float(instruction)
    elif opcode == '7':
        orinstr(instruction)
    elif opcode == '8':
        andinstr(instruction)
    elif opcode == '9':
        xor(instruction)
    elif opcode == 'a':
        rotate(instruction)
    elif opcode == 'b':
        jump(instruction)
    elif opcode == 'c':
        halt()
    else:
        print("instruction could not be completed.")


def create_instruction(a, b):
    completeinstruction = (a + b)

    return completeinstruction

# If instruction looks like 1RXY, load register R
# with the bits found in memory cell XY
def load_from_cell(instruction):
    print("Load from cell")


# If instruction looks like 2RXY, load register R
# with the bit pattern XY
def load_with(instruction):
    print("Load with pattern")
    r = registers[int(instruction[1], 16)]
    value = instruction[2:]
    r.setvalue(value)

# If instruction looks like 3RXY, store the contents
# of register R in memory cell XY
def store(instruction):
    print("Store")


# If instruction looks like 4*RS, move/copy the bit
# pattern in register R to register S
def move(instruction):
    print("Move")


# If instruction looks like 5RST, add the bit patterns
# in registers S and T and store the result in R as
# a two's complement representation
def add_complement(instruction):
    print("Add with twos complement")


# If instruction looks like 6RST, add the bit patterns
# in registers S and T and store the result in R as
# a floating-point representation
def add_float(instruction):
    print("Add with float")


# If instruction looks like 7RST, or the bit patterns
# in registers S and T and store the result in R
def orinstr(instruction):
    print("or")
    r = registers[instruction[1]]
    s = registers[instruction[2]]
    t = registers[instruction[3]]

    r.setvaluehex(int(s.getvalue(), 16)) | hex(int(t.getvalue(), 16))


# If instruction looks like 8RST, and the bit patterns
# in registers S and T and store the result in R
def andinstr(instruction):
    print("and")


# If instruction looks like 9RST, xor the bit patterns
# in registers S and T and store the result in R
def xor(instruction):
    print("xor")


# If instruction looks like AR*X, rotate the bit pattern
# in register R one bit to the right X amount of times.
# Each time place the bit that started on the low end on
# the high end.
def rotate(instruction):
    print("rotate")


# If instruction looks like BRXY, jump to the instruction
# in the memory cell at address XY if the bit pattern in
# register R is equal to the bit pattern in register 0
def jump(instruction):
    global icounter
    if instruction[1] == registers[0].getvalue():
        icounter = int(instruction, 16)

# Halt execution.
def halt():
    global complete
    complete = True

def execute():
    global icounter
    execute_instruction(cells[icounter], cells[icounter + 1])
    if not complete and len(cells) >= icounter + 3:
        execute()

def main():
    global icounter, complete

    numcells = int(input("How many memory cells would you like to have? "))

    numregisters = int(input("How many registers would you like to have? "))

    icounter = int(input("What hex value would you like to set the instruction counter at? "), 16)

    done = False

    i = 0
    while i < numcells:
        cells.append(Cell(hex(i)))
        i = i + 1

    i = 0
    while i < numregisters:
        registers.append(Cell(hex(i)))
        i = i + 1

    while not done:
        print("Memory Cells")
        for cell in cells:
            print(cell.getid(), " ", cell.getvalue())

        print("Registers")
        for register in registers:
            print(register.getid(), " ", register.getvalue())

        nextstep = input("Type r to edit a register, m to edit a memory cell, \n"
                         "e to execute or anything else to quit. ")

        if nextstep == 'r':
            which = input("Which register would you like to edit? ")

            what = "inital"
            while len(what) != 2:
                what = input("What value would you like to put into register " + which + "? ")
                if len(what) != 2 or int(what, 16) < 0 or int(what, 16) > 255:
                    print("Please enter a two letter hex value between 00 and ff.")

            registers[int(which, 16)].setvalue(what)

        elif nextstep == 'm':
            which = input("Which memory cell would you like to edit? ")

            what = "inital"
            while len(what) != 2:
                what = input("What value would you like to put into memory cell " + which + "? ")
                if len(what) != 2 or int(what, 16) < 0 or int(what, 16) > 255:
                    print("Please enter a two letter hex value between 00 and ff.")

            cells[int(which, 16)].setvalue(what)
        elif nextstep == 'e':
            print("-----EXECUTION-----")
            execute()
            if complete == True:
                print("---PROGRAM HALTED--")
                complete = False
            print("---END EXECUTION---")
        else:
            done = True


if __name__ == "__main__":
    main()

