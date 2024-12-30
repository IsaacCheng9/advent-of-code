import heapq  # noqa
import os  # noqa
from pathlib import Path
import sys  # noqa
import re  # noqa
import math  # noqa
import fileinput  # noqa
from string import ascii_uppercase, ascii_lowercase  # noqa
from collections import Counter, defaultdict, deque, namedtuple  # noqa
from itertools import (  # noqa
    count,  # noqa
    product,  # noqa
    permutations,  # noqa
    combinations,  # noqa
    combinations_with_replacement,  # noqa
)

# Add the parent directory to the PYTHONPATH.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.utils import (  # noqa
    execute_with_runtime,
    parse_input,
    parse_lines,
    parse_list_of_ints,
    parse_2d_grid_strs,
    calculate_manhattan_distance,
)


def part_one(input_file: str) -> str:
    def resolve_operand(operand):
        # Operands 0-3 represent the literal value.
        if 0 <= operand <= 3:
            return operand
        # Operand 4 represents register A's value.
        if operand == 4:
            return register_a
        # Operand 5 represents register B's value.
        if operand == 5:
            return register_b
        # Operand 6 represents register C's value.
        if operand == 6:
            return register_c
        raise ValueError("Invalid operand value.")

    input_data = parse_input(input_file)
    raw_registers, raw_program = input_data.split("\n\n")
    # Get the integer values for each register.
    register_a, register_b, register_c = map(
        int, (register.split(": ")[1] for register in raw_registers.split("\n"))
    )
    # Get the list of integers from the program.
    program = list(map(int, raw_program.split(": ")[1].split(",")))

    # Use a pointer to iterate over the program and store the output values.
    instruction_pointer = 0
    outputs = []

    # Process the instructions one at a time.
    while instruction_pointer < len(program):
        # Each instruction consists of two numbers, the opcode (what operation
        # to perform) and the operand (what value to use).
        opcode = program[instruction_pointer]
        operand = program[instruction_pointer + 1]

        # Process instructions based on the opcode.
        match opcode:
            # adv - divide A by 2^resolve_operand(operand).
            case 0:
                # Divide register A by 2^resolve_operand(operand) via right
                # shift for efficiency.
                register_a = register_a >> resolve_operand(operand)
            # bxl - XOR register B with literal operand.
            case 1:
                register_b = register_b ^ operand
            # bst - set B to resolve_operand(operand) % 8.
            case 2:
                register_b = resolve_operand(operand) % 8
            # jnz - jump to operand if A != 0.
            case 3:
                # If register A is non-zero, jump to the operand and skip
                # normal pointer increment.
                if register_a != 0:
                    instruction_pointer = operand
                    continue
            # bxc - XOR register B with register C.
            case 4:
                register_b = register_b ^ register_c
            # out - output the value modulo 8.
            case 5:
                outputs.append(resolve_operand(operand) % 8)
            # bdv - divide A by 2^resolve_operand(operand) and store in B.
            case 6:
                register_b = register_a >> resolve_operand(operand)
            # cdv - divide A by 2^resolve_operand(operand) and store in C.
            case 7:
                register_c = register_a >> resolve_operand(operand)

        instruction_pointer += 2  # Move to next instruction.

    # Return the comma-separated string of output values.
    return ",".join(map(str, outputs))


def part_two(input_file: str) -> int:
    input_data = parse_input(input_file)
    _, raw_program = input_data.split("\n\n")
    # Get the list of integers from the program.
    program = list(map(int, raw_program.split(": ")[1].split(",")))

    def reverse_engineer(program: list[int], ans: int) -> int | None:
        # Base case: if no more program to process, we've found a solution.
        if not program:
            return ans

        # Try all possible 3-bit values (0-7) for the next position.
        for t in range(8):
            # Construct the new test value by shifting left 3 bits and adding
            # new bits.
            test_val = ans << 3 | t

            # Simulate the program's operations in reverse.
            working_b = test_val % 8  # Extract bottom 3 bits
            working_b ^= 1  # First XOR operation
            shift_amount = working_b  # Save for later use
            working_c = test_val >> shift_amount  # Compute C register value
            working_b ^= 4  # Second XOR operation
            working_b ^= working_c  # Final XOR with C register

            # If this produces the number we want, recursively try to solve the
            # rest of the program.
            if working_b % 8 == program[-1]:
                sub = reverse_engineer(program[:-1], test_val)
                if sub is not None:
                    return sub

    res = reverse_engineer(program, 0)
    if res is None:
        raise ValueError("No solution found.")
    return res


if __name__ == "__main__":
    day_path = Path(__file__).parent
    input_path = day_path / "input.txt"

    print("\n--- Part One ---")
    answer1, duration1 = execute_with_runtime(part_one, str(input_path))
    print(f"Answer: {answer1}")
    print(f"Runtime: {duration1:.4f} milliseconds")

    print("\n--- Part Two ---")
    answer2, duration2 = execute_with_runtime(part_two, str(input_path))
    print(f"Answer: {answer2}")
    print(f"Runtime: {duration2:.4f} milliseconds")

    print(f"\nTotal runtime: {duration1 + duration2:.4f} milliseconds")
