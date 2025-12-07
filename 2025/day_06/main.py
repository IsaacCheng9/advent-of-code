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

import pandas as pd

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
    data = parse_lines(input_file)
    data = [line.split() for line in data]
    df = pd.DataFrame(data)
    num_cols = df.shape[1]

    total = 0
    for col_index in range(num_cols):
        # Rows 0 to n - 2 are digits, row n - 1 is the operator.
        operator = df.iloc[-1, col_index]
        nums = df.iloc[:-1, col_index].astype(int).to_numpy()
        if operator == "+":
            total += nums.sum()
        elif operator == "*":
            total += nums.prod()

    return total


def part_two(input_file: str):
    """
    Solves Part 2 by reading the input grid and processing columns right-to-left.

    The input is treated as a 2D grid of characters. We read columns from right
    to left. Consecutive non-empty columns form a problem. Within each problem,
    each column represents a number (digits read top-to-bottom) and potentially
    contains the operator in the last row. We accumulate numbers and the
    operator, then compute the result when a separator column (all spaces) is
    encountered.

    Time Complexity: O(R * C) where R is the number of rows and C is the number
    of columns (characters in the longest line).
    Space Complexity: O(R * C) to store the grid.
    """
    with open(input_file) as file:
        lines = file.read().splitlines()

    # Pad all lines to the same length.
    max_len = max(len(line) for line in lines)
    lines = [line.ljust(max_len) for line in lines]

    grid = [list(line) for line in lines]
    df = pd.DataFrame(grid)
    num_cols = df.shape[1]

    total = 0
    current_nums = []
    operator = None

    # Read right-to-left.
    for col_index in range(num_cols - 1, -1, -1):
        col_values = df.iloc[:, col_index]

        # If it's a separator column, process the problem we've built up.
        if (col_values == " ").all():
            if current_nums and operator:
                if operator == "+":
                    total += sum(current_nums)
                elif operator == "*":
                    total += math.prod(current_nums)
                current_nums = []
                operator = None
            continue

        # Otherwise build up the problem: extract number and operator.
        # Rows 0 to n - 2 are digits, row n - 1 is the operator.
        digits = "".join(char for char in col_values.iloc[:-1] if char.strip())
        operator = col_values.iloc[-1]
        if digits:
            current_nums.append(int(digits))
        if operator in ["+", "*"]:
            operator = operator

    # Process the last problem (leftmost).
    if current_nums and operator:
        if operator == "+":
            total += sum(current_nums)
        elif operator == "*":
            total += math.prod(current_nums)

    return total


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
