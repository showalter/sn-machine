# Showalter-Nutter Machine Code Simulator
This is a machine code simulator coded in Python 3 based upon the 
[Brookshear Machine](https://w3.cs.jmu.edu/cs101/unit03/bmachine.html).

## Getting Started

### Prerequisites
The Python 3 interpreter must be installed

### Installation
Open a terminal and run `git clone https:\\github.com\showalrm\sn-machine`

### Execution
Run the `__main__` module to execute the program.

## Usage
Upon execution of the program the user is prompted with the option of choosing the number of register
cells and the number of memory cells they would like. The user may choose up to 16 register cells
and up to 256 memory cells.

After configuration, the user may use the following keys to edit the cells.

- `r` - edit the contents of register cells
- `m` - edit the contents of memory cells
- `return` - step through the program
- `i` - edit the instruction counter
- `e` - execute the program
- Any other input will quit the program

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

## License
This project is licensed under the terms of the MIT license. See [LICENSE](LICENSE) for more details.

## Acknowledgement
The machine code language was created by Glenn Brookshear.