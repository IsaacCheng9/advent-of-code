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
    grid = parse_2d_grid_strs(input_file)
    num_rows = len(grid)
    num_cols = len(grid[0])
    start = grid[0].index("S")
    queue = deque([(0, start)])
    seen = set()
    num_splits = 0

    while queue:
        row, col = queue.popleft()
        if (
            row not in range(num_rows)
            or col not in range(num_cols)
            or (row, col) in seen
        ):
            continue
        seen.add((row, col))

        while row < num_rows and grid[row][col] != "^":
            row += 1
        if row == num_rows:
            continue
        if grid[row][col] == "^":
            num_splits += 1
            if col - 1 in range(num_cols):
                queue.append((row, col - 1))
            if col + 1 in range(num_cols):
                queue.append((row, col + 1))

    return num_splits


def part_two(input_file: str):
    data = parse_input(input_file)


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
