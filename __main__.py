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
    instruction = create_instruction(a.tostr(), b.tostr())
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

def load_from_cell(instruction):
    """If the instruction = 1RXY - LOAD register R with the bits found in memory cell XY"""
    r = registers[int(instruction[1], 16)]
    xy = instruction[2:]
    xy = cells[int(xy, 16)]

    r.setvalue(hex(xy.getvalue()))

def load_with(instruction):

    """If the instruction = 2RXY - LOAD register R with the hex value XY"""
    r = registers[int(instruction[1], 16)]

    value = instruction[2:]
    r.setvalue(hex(int(value, 16)))

def store(instruction):
    """If the instruction = 3RXY - STORE the contents of register R into memory cell XY"""
    r = registers[int(instruction[1], 16)]
    xy = instruction[2:]
    xy = cells[int(xy, 16)]

    xy.setvalue(hex(r.getvalue()))

def move(instruction):
    """IF instruction = 4*RS - MOVE the bit pattern found in register R into register S."""
    r = registers[int(instruction[2], 16)]
    s = registers[int(instruction[3], 16)]

    s.setvalue(hex(r.getvalue()))

def add_complement(instruction):
    """IF instruction = 5RST - ADD the bit patterns in register S and T and store the result in register R"""
    r = registers[int(instruction[1], 16)]
    s = registers[int(instruction[2], 16)]
    t = registers[int(instruction[3], 16)]

    sval = s.getvalue()
    tval = t.getvalue()

    if sval > 127:
        sval = - sval
    if tval > 127:
        tval = - tval

    value = sval + tval

    if value > 127:
        value = - value

    r.setvalue(hex(value))

# If instruction looks like 6RST, add the bit patterns
# in registers S and T and store the result in R as
# two's complement. This may be updated later to add
# numbers as floats, but precision with 8 bits is not
# great, and it's hard to see situations where this
# little precision is useful.
def add_float(instruction):
    add_complement(instruction)

def orinstr(instruction):
    """If instruction = 7RST - OR the bit patterns in register S and T and store the result in R"""
    r = registers[int(instruction[1], 16)]
    s = registers[int(instruction[2], 16)]
    t = registers[int(instruction[3], 16)]

    r.setvalue(hex(s.getvalue() | t.getvalue()))

def andinstr(instruction):
    """If instruction = 8RST - AND the bit patterns in S and T and store the result in R"""
    r = registers[int(instruction[1], 16)]
    s = registers[int(instruction[2], 16)]
    t = registers[int(instruction[3], 16)]

    r.setvalue(hex(s.getvalue() & t.getvalue()))


# If instruction looks like 9RST, xor the bit patterns
# in registers S and T and store the result in R
def xor(instruction):
    """If instruction = 9RST - XOR the bit patterns in registers S and T and store the result in R"""
    r = registers[int(instruction[1], 16)]
    s = registers[int(instruction[2], 16)]
    t = registers[int(instruction[3], 16)]

    r.setvalue(hex(s.getvalue() ^ t.getvalue()))

def rotate(instruction):
    """IF instruction = AR*X - ROTATE the bit pattern in register R (one bit to the right 'X' amount of times) Each time place the bit that started on the low end on the high end"""
    bits = 8

    r = registers[int(instruction[1], 16)]
    x = registers[int(instruction[3], 16)].getvalue()

    n = x % bits
    a = r.getvalue() >> n
    b = r.getvalue() << ((bits - n) % 256)
    value = a | b
    r.setvalue(hex(value))

def jump(instruction):
    """If instruction = BRXY - JUMP the instruction in the memory cell at address XY if the bit pattern in register X is equal to the bit pattern in register 0"""
    global icounter
    if registers[int(instruction[1], 16)].getvalue() == registers[0].getvalue():
        icounter = int(instruction[2:], 16)

def halt():
    """Halt Execution"""
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
            print(cell.getid(), " ", cell.tostr())

        print("Registers")
        for register in registers:
            print(register.getid(), " ", register.tostr())

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
            if complete:
                print("---PROGRAM HALTED--")
                complete = False
            print("---END EXECUTION---")
        else:
            done = True


if __name__ == "__main__":
    main()

