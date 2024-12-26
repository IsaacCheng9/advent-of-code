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


# Takes ~200x longer than the optimised solution - measured 135ms vs 0.7ms.
def part_one_bruteforce(file_name: str) -> int:
    input_data = parse_input(file_name)
    blocks = input_data.split("\n\n")
    num_tokens: int = 0

    for block in blocks:
        lines = block.strip().split("\n")
        # Parse button A
        ax = int(lines[0].split("X+")[1].split(",")[0])
        ay = int(lines[0].split("Y+")[1])
        # Parse button B
        bx = int(lines[1].split("X+")[1].split(",")[0])
        by = int(lines[1].split("Y+")[1])
        # Parse the prize
        px = int(lines[2].split("X=")[1].split(",")[0])
        py = int(lines[2].split("Y=")[1])

        cur_tokens = float("inf")
        # Try every combination of tokens from 0 to 100 of each button and
        # track the minimum number of tokens needed to reach the prize.
        for i in range(101):
            for j in range(101):
                if (ax * i) + (bx * j) == px and (ay * i) + (by * j) == py:
                    cur_tokens = min(cur_tokens, (i * 3) + j)
        # Avoid adding the value if we didn't find a valid token combination.
        if cur_tokens != float("inf"):
            num_tokens += cur_tokens  # type: ignore

    return num_tokens


def part_one(file_name: str) -> int:
    input_data = parse_input(file_name)
    blocks = input_data.split("\n\n")
    num_tokens = 0

    for block in blocks:
        lines = block.strip().split("\n")
        # Parse button A.
        ax = int(lines[0].split("X+")[1].split(",")[0])
        ay = int(lines[0].split("Y+")[1])
        # Parse button B.
        bx = int(lines[1].split("X+")[1].split(",")[0])
        by = int(lines[1].split("Y+")[1])
        # Parse the prize.
        px = int(lines[2].split("X=")[1].split(",")[0])
        py = int(lines[2].split("Y=")[1])

        # Solve the system of linear equations - we have two equations and two
        # unknowns, so we can solve it using Cramer's rule.
        # (ax)s + (bx)t = px
        # (ay)s + (by)t = py
        # Make it so that t is the same in both equations - multiply the
        # top by by and the bottom by bx:
        # (ax)(by)s + (bx)(by)t = px(by)
        # (ay)(bx)s + (bx)(by)t = py(bx)
        # Subtract the second from the first equation to solve for s:
        # (ax)(by)s - (ay)(bx)s = px(by) - py(bx)
        # s(ax(by) - ay(bx)) = px(by) - py(bx)
        # s = (px(by) - py(bx)) / (ax(by) - ay(bx))
        s = ((px * by) - (py * bx)) / ((ax * by) - (ay * bx))
        # Now that we have s, we can solve for t:
        # (ax)s + (bx)t = px
        # (bx)t = px - (ax)s
        # t = (px - (ax)s) / bx
        t = (px - (ax * s)) / bx
        # s and t need to be integers between 0 and 100 inclusive to be valid.
        if s % 1 == t % 1 == 0 and s <= 100 and t <= 100:
            num_tokens += int(s * 3 + t)

    return num_tokens


def part_two(file_name: str) -> int:
    input_data = parse_input(file_name)
    blocks = input_data.split("\n\n")
    num_tokens = 0

    for block in blocks:
        lines = block.strip().split("\n")
        # Parse button A.
        ax = int(lines[0].split("X+")[1].split(",")[0])
        ay = int(lines[0].split("Y+")[1])
        # Parse button B.
        bx = int(lines[1].split("X+")[1].split(",")[0])
        by = int(lines[1].split("Y+")[1])
        # Parse the prize.
        px = int(lines[2].split("X=")[1].split(",")[0])
        py = int(lines[2].split("Y=")[1])
        px += 10000000000000
        py += 10000000000000

        # Solve the system of linear equations - we have two equations and two
        # unknowns, so we can solve it using Cramer's rule.
        # (ax)s + (bx)t = px
        # (ay)s + (by)t = py
        # Make it so that t is the same in both equations - multiply the
        # top by by and the bottom by bx:
        # (ax)(by)s + (bx)(by)t = px(by)
        # (ay)(bx)s + (bx)(by)t = py(bx)
        # Subtract the second from the first equation to solve for s:
        # (ax)(by)s - (ay)(bx)s = px(by) - py(bx)
        # s(ax(by) - ay(bx)) = px(by) - py(bx)
        # s = (px(by) - py(bx)) / (ax(by) - ay(bx))
        s = (px * by - py * bx) / (ax * by - ay * bx)
        # Now that we have s, we can solve for t:
        # (ax)s + (bx)t = px
        # (bx)t = px - (ax)s
        # t = (px - (ax)s) / bx
        t = (px - ax * s) / bx
        # s and t need to be integers to be valid.
        if s % 1 == t % 1 == 0:
            num_tokens += int(s * 3 + t)

    return num_tokens


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
