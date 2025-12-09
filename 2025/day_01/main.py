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
    num_zeroes = 0
    # Track rotation in range [0, 99], starting at 50.
    cur_rotation = 50

    for line in input_data:
        direction = line[0]
        distance = int(line[1:])

        if direction == "L":
            cur_rotation = (cur_rotation - distance) % 100
        else:
            cur_rotation = (cur_rotation + distance) % 100

        if cur_rotation == 0:
            num_zeroes += 1

    return num_zeroes


def part_two(input_file: str):
    input_data = parse_lines(input_file)
    num_zeroes = 0
    # Track rotation in range [0, 99], starting at 50.
    cur_rotation = 50

    for line in input_data:
        direction = line[0]
        distance = int(line[1:])

        if direction == "L":
            # Moving left from cur_rotation, we cross 0 at distances:
            # cur_rotation, cur_rotation + 100, cur_rotation + 200, etc.
            # Crossings = ((distance - cur_rotation) // 100)) + 1
            #           = (distance + 100 - cur_rotation) // 100
            # e.g. from position 50, L150:
            # (150 + 100 - 50) // 100 = 200 // 100 = 2
            # Exception: when cur_rotation = 0, we're already at the boundary,
            # so first crossing is at 100, not 0.
            if cur_rotation == 0:
                num_zeroes += distance // 100
            elif distance >= cur_rotation:
                num_zeroes += (distance + 100 - cur_rotation) // 100
            cur_rotation = (cur_rotation - distance) % 100
        else:
            # Moving right, total position = cur_rotation + distance.
            # We cross 0 at multiples of 100: 100, 200, 300, etc.
            # Crossings = (cur_rotation + distance) // 100
            # Works for all cases: when cur_rotation = 0, we cross at 100,
            # 200, etc., giving distance // 100
            num_zeroes += (cur_rotation + distance) // 100
            cur_rotation = (cur_rotation + distance) % 100

    return num_zeroes


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
