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
    execute_with_runtime,
    parse_input,
    parse_lines,
    parse_list_of_ints,
    parse_2d_grid_strs,
    calculate_manhattan_distance,
)


def part_one(file_name: str) -> int:
    with open(file_name) as file:
        data = file.read().splitlines()

    pairs = [list(map(int, line.split())) for line in data]
    left_nums = sorted([pair[0] for pair in pairs])
    right_nums = sorted([pair[1] for pair in pairs])
    total_distance_diff = sum(abs(a - b) for a, b in zip(left_nums, right_nums))

    return total_distance_diff


def part_two(file_name: str) -> int:
    with open(file_name) as file:
        data = file.read().splitlines()

    pairs = [list(map(int, line.split())) for line in data]
    left_nums = [pair[0] for pair in pairs]
    right_nums = [pair[1] for pair in pairs]
    right_counter = Counter(right_nums)
    similarity_score = sum(num * right_counter[num] for num in left_nums)

    return similarity_score


if __name__ == "__main__":
    day_path = Path(__file__).parent
    input_path = day_path / "input.txt"

    print("--- Part One ---")
    answer1, duration1 = execute_with_runtime(part_one, str(input_path))
    print(f"Answer: {answer1}")
    print(f"Runtime: {duration1:.4f} milliseconds")

    print("\n--- Part Two ---")
    answer2, duration2 = execute_with_runtime(part_two, str(input_path))
    print(f"Answer: {answer2}")
    print(f"Runtime: {duration2:.4f} milliseconds")

    print(f"\nTotal runtime: {duration1 + duration2:.4f} milliseconds")