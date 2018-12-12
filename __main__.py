"""
The main module contains the main function and other functions for constructing cells and executing machine code

Copyright (c) 2018 Ryan Showalter and Cole Nutter under the terms of the MIT License

Attributes:
    cells (list of Cell): A list of all memory cells
    registers (list of Cell): A list of all registers
    icounter (int): The numeric location of the execution counter
    complete (bool): True when program is halted; false otherwise

"""

from display import display
from processor import Cell

cells = []
registers = []

icounter = None

complete = False


def execute_instruction(a, b):
    """ Execute the contents of two memory cells.

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
    """ Create a full instruction from the contents of two cells

    Args:
        a (str): The string for the first half of the instruction
        b (str): The string for the second half of the instruction

    Returns:
        str: The complete instruction
    """

    completeinstruction = (a + b)

    return completeinstruction


def load_from_cell(instruction):
    """ Load a register with the contents of a memory cell

    The instruction should look like (opcode)RXY, where R is the register being loaded, and
    XY is the memory cell with the contents being moved.

    Args:
        instruction (str): the instruction being executed, in this case it starts with a 1
    """

    r = registers[int(instruction[1], 16)]
    xy = instruction[2:]
    xy = cells[int(xy, 16)]

    r.setvalue(hex(xy.getvalue()))


def load_with(instruction):
    """ Load a register with a specific value

    The instruction should look like (opcode)RXY, where R is the register being loaded, and
    XY is the pattern being put into the register.

    Args:
        instruction (str): the instruction being executed, in this case it starts with a 2
    """

    r = registers[int(instruction[1], 16)]

    value = instruction[2:]
    r.setvalue(hex(int(value, 16)))


def store(instruction):
    """ Store the contents of a register in a memory cell

    The instruction should look like (opcode)RXY, where R is the register with contents being stored,
    and XY is the memory cell where the contents are being stored.

    Args:
        instruction (str): the instruction being executed, in this case it starts with a 3
    """

    r = registers[int(instruction[1], 16)]
    xy = instruction[2:]
    xy = cells[int(xy, 16)]

    xy.setvalue(hex(r.getvalue()))


def move(instruction):
    """ Move/copy the contents of a register to another register

    The instruction should look like (opcode)*RS, where R is the register being copied, and S
    is the register being copied to.

    Args:
        instruction (str): the instruction being executed, in this case it starts with a 4
    """

    r = registers[int(instruction[2], 16)]
    s = registers[int(instruction[3], 16)]

    s.setvalue(hex(r.getvalue()))


def add_complement(instruction):
    """ Add the values of two registers in twos complement notation and place the result in a register.

    The instruction should look like (opcode)RST, where S and T are the registers whose contents are being
    added, and R is the register where the result is stored.

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


def add_float(instruction):
    """ Add two registers together. This passes the instruction to add_complement() for now.

    The instruction should look like (opcode)RST, where S and T are the registers whose contents are being
    added, and R is the register where the result is being stored.

    Args:
        instruction (str): the instruction being executed, in this case it starts with a 6
    """

    add_complement(instruction)


def orinstr(instruction):
    """ Or the bit patterns in two registers together.

    The instruction should look like (opcode)RST, where S and T are the registers whose contents are
    used as operands for the or operation, and R is the register where the result is stored.

    Args:
        instruction (str): the instruction being executed, in this case it starts with a 7

    """
    r = registers[int(instruction[1], 16)]
    s = registers[int(instruction[2], 16)]
    t = registers[int(instruction[3], 16)]

    r.setvalue(hex(s.getvalue() | t.getvalue()))


def andinstr(instruction):
    """ And the bit patterns in two registers together.

    The instruction should look like (opcode)RST, where S and T are the registers whose contents are
    used as operands for the and operation, and R is the register where the result is stored.

    Args:
        instruction (str): the instruction being executed, in this case it starts with an 8
    """

    r = registers[int(instruction[1], 16)]
    s = registers[int(instruction[2], 16)]
    t = registers[int(instruction[3], 16)]

    r.setvalue(hex(s.getvalue() & t.getvalue()))


def xor(instruction):
    """ Xor the bit patterns in two registers together.

    The instruction should look like (opcode)RST, where S and T are the registers whose contents are
    used as operands for the xor operation, and R is the register where the result is stored.

    Args:
        instruction (str): the instruction being executed, in this case it starts with a 9
    """

    r = registers[int(instruction[1], 16)]
    s = registers[int(instruction[2], 16)]
    t = registers[int(instruction[3], 16)]

    r.setvalue(hex(s.getvalue() ^ t.getvalue()))


def rotate(instruction):
    """ Rotate the contents of a register to the right a number of times, with bits that fall off the
    low order end being replaced on the high order end.

    The instruction should look like (opcode)R*X, where R is the register whose contents are being rotated,
    and X is the number of rotations done.

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
    """ Conditionally jump to a different memory cell, by changing the instruction counter.

    The instruction should look like (opcode)RXY, where XY is the register being jumped to, if
    the contents of register R are equal to the contents of register 0.

    Args:
        instruction (str): the instruction being executed, in this case it starts with a B
    """

    global icounter
    if registers[int(instruction[1], 16)].getvalue() == registers[0].getvalue():
        icounter = int(instruction[2:], 16)


def halt():
    """ Halt the execution of the program"""

    global complete
    complete = True


def execute(step):
    """ Execute the operation specified by the instruction counter

    Args:
        step (bool): if True, execute once; otherwise, execute until completion.
    """

    global icounter
    if len(cells) >= icounter + 1:
        execute_instruction(cells[icounter], cells[icounter + 1])
    if not complete and not step and len(cells) >= icounter + 3:
        execute(False)


def main():
    """ The main function constructs memory and register cells and allows the user to edit them
    and execute the contents of those cells"""

    global icounter, complete
    numcells = -1
    numregisters = -1

    # Prompt for the desired number of memory cells and registers
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

        # Edit register cells
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

        # Edit memory cells
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

        # Edit the instruction counter
        elif nextstep == 'i':
            icounter = int(input("What hex value would you like to set the instruction "
                                 "counter at? "), 16)

        # Execute until completion
        elif nextstep == 'e':
            print("-----EXECUTION-----")
            execute(False)
            if complete:
                print("---PROGRAM HALTED--")
                complete = False
            print("---END EXECUTION---")

        # Execute once
        elif nextstep == '':
            execute(True)
        else:
            done = True


if __name__ == "__main__":
    """Execute the main function"""
    main()
