"""
Advent of Code solution template with enhanced utilities.
"""

import os  # NOQA
from pathlib import Path
import sys  # NOQA
import re  # NOQA
import math  # NOQA
import fileinput  # NOQA
from string import ascii_uppercase, ascii_lowercase  # NOQA
from collections import Counter, defaultdict, deque, namedtuple  # NOQA
from itertools import (  # NOQA
    count,  # NOQA
    product,  # NOQA
    permutations,  # NOQA
    combinations,  # NOQA
    combinations_with_replacement,  # NOQA
)

# Add the parent directory to the PYTHONPATH.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.utils import (  # NOQA
    run_with_timing,
    parse_input,
    parse_lines,
    parse_ints,
    parse_2d_grid,
    calculate_manhattan_distance,
)


def part_one(file_name: str) -> int:
    data = parse_input(file_name)
    res = 0

    return res


def part_two(file_name: str) -> int:
    data = parse_input(file_name)
    res = 0

    return res


if __name__ == "__main__":
    day_path = Path(__file__).parent
    input_path = day_path / "input.txt"

    print("--- Part One ---")
    answer1, duration1 = run_with_timing(part_one, str(input_path))
    print(f"Answer: {answer1}")
    print(f"Time: {duration1:.4f} seconds")

    print("\n--- Part Two ---")
    answer2, duration2 = run_with_timing(part_two, str(input_path))
    print(f"Answer: {answer2}")
    print(f"Time: {duration2:.4f} seconds")

    print(f"\nTotal time: {duration1 + duration2:.4f} seconds")
