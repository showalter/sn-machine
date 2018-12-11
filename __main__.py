from display import display
from processor import Cell

cells = []
registers = []

icounter = None

complete = False


def execute_instruction(a, b):
    """Execute the contents of two memory cells.

    Args:
        a (cell): The cell that hold the first half of the instruction
        b (cell): The cell that hold the second half of the instruction
    """
    global icounter
    instruction = create_instruction(a.tostr(), b.tostr())
    opcode = instruction[0]
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
    """Creates a full instruction from the contents of two cells

    Args:
        a (str): The string for the first half of the instruction
        b (str): The string for the second half of the instruction

    Returns:
        str: The complete instruction
    """
    completeinstruction = (a + b)

    return completeinstruction


def load_from_cell(instruction):
    """ If instruction looks like 1RXY
    load register R with the bits found in memory cell XY

    Args:
        instruction (str): the instruction being executed, in this case it starts with a 1
    """
    r = registers[int(instruction[1], 16)]
    xy = instruction[2:]
    xy = cells[int(xy, 16)]

    r.setvalue(hex(xy.getvalue()))


def load_with(instruction):
    """If instruction looks like 2RXY
    LOAD register R with the bit pattern XY

    Args:
        instruction (str): the instruction being executed, in this case it starts with a 2

    """

    r = registers[int(instruction[1], 16)]

    value = instruction[2:]
    r.setvalue(hex(int(value, 16)))


def store(instruction):
    """ If instruction looks like 3RXY
    STORE the contents of register R in memory cell XY

    Args:
        instruction (str): the instruction being executed, in this case it starts with a 3

    """
    r = registers[int(instruction[1], 16)]
    xy = instruction[2:]
    xy = cells[int(xy, 16)]

    xy.setvalue(hex(r.getvalue()))


def move(instruction):
    """If instruction look slike 4*RS
    MOVE the bit pattern in register R to register S

    Args:
        instruction (str): the instruction being executed, in this case it starts with a 4

    """
    r = registers[int(instruction[2], 16)]
    s = registers[int(instruction[3], 16)]

    s.setvalue(hex(r.getvalue()))


def add_complement(instruction):
    """If instruction looks like 5RST
    ADD the bit patterns in registers S and T and store the result in R
    as a two's complement representation

    Args:
        instruction (str): the instruction being executed, in this case it starts with a 5

    """
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
    """If instruction looks like 7RST
    OR the bit patterns in registers S and T and store the result in R

    Args:
        instruction (str): the instruction being executed, in this case it starts with a 7

    """
    r = registers[int(instruction[1], 16)]
    s = registers[int(instruction[2], 16)]
    t = registers[int(instruction[3], 16)]

    r.setvalue(hex(s.getvalue() | t.getvalue()))


def andinstr(instruction):
    """If instruction looks like 8RST
    AND the bit patterns in registers S and T and store the result in R

    Args:
        instruction(str): the instruction being executed, in this case it starts with a 8

    """
    r = registers[int(instruction[1], 16)]
    s = registers[int(instruction[2], 16)]
    t = registers[int(instruction[3], 16)]

    r.setvalue(hex(s.getvalue() & t.getvalue()))


def xor(instruction):
    """If instruction looks like 9RST
    XOR the bit patterns in registers S and T and store the result in R

    Args:
        instruction (str): the instruction being executed, in this case it starts with a 9

        """
    r = registers[int(instruction[1], 16)]
    s = registers[int(instruction[2], 16)]
    t = registers[int(instruction[3], 16)]

    r.setvalue(hex(s.getvalue() ^ t.getvalue()))


def rotate(instruction):
    """If instruction looks like AR*X
    ROTATE the bit pattern in register R one bit to the right X amount of times.
    (Each time rotated place the bit that started on the low end on the high end)

    Args:
        instruction (str): the instruction being executed, in this case it starts with an A

        """
    bits = 8

    r = registers[int(instruction[1], 16)]
    x = registers[int(instruction[3], 16)].getvalue()

    n = x % bits
    a = r.getvalue() >> n
    b = r.getvalue() << ((bits - n) % 256)
    value = a | b
    r.setvalue(hex(value))


def jump(instruction):
    """If instruction looks like BRXY
    JUMP to the instruction in memory cell at address XY if the bit pattern in
    register R is equal to the bit pattern in register 0

    Args:
        instruction (str): the instruction being executed, in this case it starts with a B

    """
    global icounter
    if registers[int(instruction[1], 16)].getvalue() == registers[0].getvalue():
        icounter = int(instruction[2:], 16)


def halt():
    """If instruction looks like C***
    HALT the execution of the program

    Args:
        instruction (str): the instruction being executed, in this case it starts with a C

    """
    global complete
    complete = True


def execute(step):
    global icounter
    if len(cells) >= icounter + 1:
        execute_instruction(cells[icounter], cells[icounter + 1])
    if not complete and not step and len(cells) >= icounter + 3:
        execute(False)


def main():
    global icounter, complete
    numcells = -1
    numregisters = -1

    while numcells < 1 or numcells > 256:
        numcells = int(input("How many memory cells would you like to have? "))

    while numregisters < 1 or numregisters > 16:
        numregisters = int(input("How many registers would you like to have? "))

    icounter = int(input("What hex value would you like to set the instruction "
                         "counter at? "), 16)

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
        display(cells, registers, icounter)

        nextstep = input("Type r to edit a register, m to edit a memory cell, \n"
                         "e to execute, i to edit the instruction counter, \n"
                         "enter to step, or anything else to quit. ")

        if nextstep == 'r':
            which = None
            while which is None or which < 0 or which > len(registers):
                which = input("Which register would you like to edit? ")
                which = int(which, 16)

            what = input("What value would you like to put into register " +
                         str(hex(which))[2:] + "? ")

            i = 0
            j = 0
            n = len(what)
            while i < n:
                registers[which + j].setvalue(what[0 + i:2 + i])
                i += 2
                j += 1

        elif nextstep == 'm':
            which = None
            while which is None or which < 0 or which > len(cells):
                which = input("Which memory cell would you like to edit? ")
                which = int(which, 16)

            what = input("What value would you like to put into memory cell " +
                         str(hex(which))[2:] + "? ")

            i = 0
            j = 0
            n = len(what)
            while i < n:
                cells[which + j].setvalue(what[0 + i:2 + i])
                i += 2
                j += 1

        elif nextstep == 'i':
            icounter = int(input("What hex value would you like to set the instruction "
                                 "counter at? "), 16)
            
        elif nextstep == 'e':
            print("-----EXECUTION-----")
            execute(False)
            if complete:
                print("---PROGRAM HALTED--")
                complete = False
            print("---END EXECUTION---")

        elif nextstep == '':
            execute(True)
        else:
            done = True


if __name__ == "__main__":
    main()
