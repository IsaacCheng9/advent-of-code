import fileinput  # noqa
import heapq  # noqa
import math  # noqa
import numpy as np
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
from scipy.optimize import linprog

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
    lines = parse_lines(input_file)
    total_presses = 0

    for line in lines:
        target, *moves, counters = line.split()
        # Parse target as a set of light indices that should be on.
        target = {index for index, light in enumerate(target[1:-1]) if light == "#"}
        buttons = [set(map(int, button[1:-1].split(","))) for button in moves]
        counters = list(map(int, counters[1:-1].split(",")))

        found = False
        # Try combinations of increasing size (1 button, 2 buttons, etc).
        for num_buttons in range(1, len(buttons) + 1):
            for attempt in combinations(buttons, num_buttons):
                lights = set()
                # XOR simulates toggling: overlapping lights between buttons
                # cancel out. e.g. {1, 3} ^ {2, 3} = {1, 2} (light 3 cancels).
                for button in attempt:
                    lights ^= button
                # First match is optimal since we try the smallest combinations
                # first.
                if lights == target:
                    total_presses += num_buttons
                    found = True
                    break

            if found:
                break

    return total_presses


def part_two(input_file: str):
    lines = parse_lines(input_file)
    total_presses = 0

    for line in lines:
        _, *moves, counters = line.split()
        buttons = [set(map(int, button[1:-1].split(","))) for button in moves]
        counters = list(map(int, counters[1:-1].split(",")))

        num_buttons = len(buttons)
        num_counters = len(counters)

        # Objective: minimise total button presses: x0 + x1 + ... + xn,
        c = [1] * num_buttons

        # Build a constraint matrix A_eq, where A[i][j] = 1 if button j affects
        # counter i.
        A_eq = np.zeros((num_counters, num_buttons))
        for j, button_indices in enumerate(buttons):
            for i in button_indices:
                A_eq[i, j] = 1

        # Solve the linear program: minimise c.x, subject to A_eq.x = counters,
        # x >= 0, x is an integer.
        res = linprog(
            c,
            A_eq=A_eq,
            b_eq=counters,
            integrality=1,  # Forces solutions to be integers.
        )

        if res.success:
            total_presses += int(round(res.fun))

    return total_presses


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
