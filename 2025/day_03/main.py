import fileinput  # noqa
import heapq  # noqa
import math  # noqa
import os  # noqa
import re  # noqa
import sys  # noqa
from collections import Counter, defaultdict, deque, namedtuple  # noqa
from functools import cache  # noqa
from itertools import (  # noqa
    combinations,
    combinations_with_replacement,
    count,
    permutations,
    product,
)
from bisect import bisect_left, bisect_right  # noqa
from math import gcd, lcm  # noqa
from pathlib import Path  # noqa
from string import ascii_lowercase, ascii_uppercase  # noqa

# Add the parent directory to the PYTHONPATH.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.utils import (  # noqa
    calculate_manhattan_distance,
    execute_with_runtime,
    parse_2d_grid_strs,
    parse_input,
    parse_lines,
    parse_list_of_ints,
)


def part_one(input_file: str):
    input_data = parse_lines(input_file)
    total_voltage = 0

    for line in input_data:
        length = len(line)

        # Precompute max digit to the right of each position.
        max_to_right = [""] * length
        max_to_right[-1] = ""  # No digit to the right of the last position.
        max_after = "0"
        for index in range(length - 2, -1, -1):
            max_to_right[index] = max_after
            max_after = max(max_after, line[index])

        # Find the best 2-digit number.
        max_voltage = 0
        for index in range(length - 1):
            voltage = int(line[index] + max_to_right[index])
            max_voltage = max(max_voltage, voltage)

        total_voltage += max_voltage

    return total_voltage


def part_two(input_file: str):
    input_data = parse_lines(input_file)
    total_voltage = 0

    for line in input_data:
        length = len(line)
        voltage = []
        start_index = 0

        for _ in range(12):
            cur_max = "0"
            max_index = start_index
            # Ensure we have enough digits to form a 12-digit number.
            digits_needed = 12 - len(voltage)
            end_index = length - digits_needed + 1

            # Find the max digit in the remaining digits.
            for index in range(start_index, end_index):
                if line[index] > cur_max:
                    cur_max = line[index]
                    max_index = index

            voltage.append(cur_max)
            # Move past the selected digit for the next iteration.
            start_index = max_index + 1

        total_voltage += int("".join(voltage))

    return total_voltage


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
