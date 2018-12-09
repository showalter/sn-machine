# Showalter-Nutter Machine Code Simulator
This is a machine code simulator coded in Python 3 based upon the 
[Brookshear Machine](https://w3.cs.jmu.edu/cs101/unit03/bmachine.html).

### Language Description Table

|Op-Code   | Operand | Description |
|:--------:|:-------:|-------------|
|1         | RXY     | LOAD register R with the bits found in memory cell XY |
|2         | RXY     | LOAD register R with the hex value XY|
|3         | RXY     | STORE the contents found in register R in the memory cell XY |
|4         | *RS     | MOVE the bit pattern found in register R to register S | 
|5         | RST     | ADD the bit patterns in registers S and T and put the result in register R in a two’s complement complement representation |
|6         | RST     | ADD the bit patterns in registers S and T and put the result in register R in a floating-point notation |
|7         | RST     | OR the bit patterns in registers S and T and put the result in register R |
|8         | RST     | AND  the bit patterns in registers S and T and place the result in register R |
|9         | RST     | XOR the bit patterns in registers S and T and place the result in register R |
|A         | R*X     | ROTATE the bit pattern in register R one bit to the right X amount of times. Each time placing the bit that started on the low end on the high end.
|B         | RXY     | JUMP to the instruction located in the memory cell at address XY if the bit pattern in register R is equal to the bit pattern in register number 0. Otherwise, continue with the normal sequence of execution. (The jump is implemented by copying XY into the program counter during the execute phase.) |
|C         | ***     | HALT |

##How It Works

Upon execution of the program you are prompted to choose how many register cell's you would like
and how many memory cells you would like.

The values of the register cell that may be chosen are 1-16

The values that are allowed to be chosen for memory cells may be 0-255

You are now able to edit the contents of the cells and after having doing so are able to run your
code.
