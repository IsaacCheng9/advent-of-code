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
    input_data = parse_input(input_file)
    id_ranges = input_data.split(",")
    max_id = 0

    for bounds in id_ranges:
        _, upper = bounds.split("-")
        max_id = max(max_id, int(upper))

    repeated_ids = set()
    max_repeated_id = 0
    cur_lower = 1
    cur_upper = 9
    while max_repeated_id < max_id:
        for cur_digit in range(cur_lower, cur_upper + 1):
            repeated_id = int(str(cur_digit) * 2)
            if repeated_id > max_id:
                max_repeated_id = repeated_id
                break
            repeated_ids.add(repeated_id)

        if max_repeated_id >= max_id:
            break
        cur_lower *= 10
        cur_upper = (cur_upper * 10) + 9

    invalid_ids = set()
    for bounds in id_ranges:
        lower, upper = map(int, bounds.split("-"))
        for repeated_id in repeated_ids:
            if lower <= repeated_id <= upper:
                invalid_ids.add(repeated_id)

    return sum(invalid_ids)


def part_two(input_file: str):
    input_data = parse_input(input_file)
    id_ranges = input_data.split(",")
    max_id = 0

    for bounds in id_ranges:
        _, upper = bounds.split("-")
        max_id = max(max_id, int(upper))

    repeated_ids = set()
    cur_lower = 1
    cur_upper = 9

    while int(str(cur_lower) * 2) <= max_id:
        for cur_digit in range(cur_lower, cur_upper + 1):
            repeated_id = cur_digit
            while True:
                repeated_id = int(str(repeated_id) + str(cur_digit))
                if repeated_id > max_id:
                    break
                repeated_ids.add(repeated_id)

        cur_lower *= 10
        cur_upper = (cur_upper * 10) + 9

    invalid_ids = set()
    for bounds in id_ranges:
        lower, upper = map(int, bounds.split("-"))
        for repeated_id in repeated_ids:
            if lower <= repeated_id <= upper:
                invalid_ids.add(repeated_id)

    return sum(invalid_ids)


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
