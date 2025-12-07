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
    data = parse_input(input_file)
    id_ranges, available_ids = data.split("\n\n")
    id_ranges = [
        [int(num) for num in id_range.split("-")] for id_range in id_ranges.splitlines()
    ]
    available_ids = [int(num) for num in available_ids.splitlines()]

    num_fresh_ids = 0
    for cur_id in available_ids:
        for lower_bound, upper_bound in id_ranges:
            if lower_bound <= int(cur_id) <= upper_bound:
                num_fresh_ids += 1
                break

    return num_fresh_ids


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
