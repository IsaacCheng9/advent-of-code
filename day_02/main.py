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
    def is_safe(levels):
        diffs = [x - y for x, y in zip(levels, levels[1:])]
        return all(1 <= x <= 3 for x in diffs) or all(-1 >= x >= -3 for x in diffs)

    res = 0

    for report in open(file_name):
        levels = list(map(int, report.split()))
        if is_safe(levels):
            res += 1

    return res


def part_two(file_name: str) -> int:
    def is_safe(levels):
        diffs = [x - y for x, y in zip(levels, levels[1:])]
        return all(1 <= x <= 3 for x in diffs) or all(-1 >= x >= -3 for x in diffs)

    res = 0

    for report in open(file_name):
        levels = list(map(int, report.split()))
        n = len(levels)
        if any(is_safe(levels[:index] + levels[index + 1 :]) for index in range(n)):
            res += 1

    return res


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