def describe(a, b):
    """Displays an explanation of the instruction

    Args:
        a (str): The string of the first half of the description
        b (str): The string of the second half of the description

    Returns:
        The complete description

    """
    instruction = a + b
    opcode = instruction[0]

    if opcode == '1':
        result = "LOAD register {} with the value in register {}"\
                 .format(instruction[1], instruction[2:])
    elif opcode == '2':
        result = "LOAD register {} with the value {}"\
                 .format(instruction[1], instruction[2:])
    elif opcode == '3':
        result = "STORE the the value in register {} in memory cell {}"\
                 .format(instruction[1], instruction[2:])
    elif opcode == '4':
        result = "MOVE the value in register {} to register {}"\
                 .format(instruction[2], instruction[3])
    elif opcode == '5' or opcode == '6':
        result = "ADD the values in registers {} and {} in twos complement "\
                 "notation and place the result in register {}"\
                 .format(instruction[2], instruction[3], instruction[1])
    elif opcode == '7':
        result = "OR the values in registers {} and {} and place the result "\
                 "in register {}".format(instruction[2], instruction[3],
                                         instruction[1])
    elif opcode == '8':
        result = "AND the values in registers {} and {} and place the result "\
                 "in register {}".format(instruction[2], instruction[3],
                                         instruction[1])
    elif opcode == '9':
        result = "XOR the values in registers {} and {} and place the result "\
                 "in register {}".format(instruction[2], instruction[3],
                                         instruction[1])
    elif opcode == 'a':
        result = "ROTATE the bit pattern in register {} {} times"\
                 .format(instruction[1], instruction[3])
    elif opcode == 'b':
        result = "JUMP to the instruction at memory cell {} if the bit pattern "\
                 " in register {} is equal to the bit pattern in register 0"\
                 .format(instruction[2:], instruction[1])
    elif opcode == 'c':
        result = "HALT execution"
    else:
        result = ""

    return result


def display(cells, registers, icounter):
    print("Memory Cells")
    i = 0
    for cell in cells:
        print(cell.getid(), " ", cell.tostr(), end=' ')
        if i % 2 == 0 and len(cells) > i + 1:
            print(describe(cells[i].tostr(), cells[i + 1].tostr()), end='')
        i += 1
        print("")

    print("Registers")
    for register in registers:
        print(register.getid(), " ", register.tostr())

    print("Instruction counter: ", str(hex(icounter))[2:])
