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
    lines = parse_lines(input_file)
    total_presses = 0

    # Process each machine.
    for line in lines:
        target, *moves, counters = line.split()
        # Create a set representing the lights that should be on.
        target = {index for index, light in enumerate(target[1:-1]) if light == "#"}
        buttons = [set(map(int, button[1:-1].split(","))) for button in moves]
        counters = list(map(int, counters[1:-1].split(",")))

        found = False
        # Try combinations of increasing size (1 button, 2 buttons, etc).
        for num_buttons in range(1, len(buttons) + 1):
            for attempt in combinations(buttons, num_buttons):
                lights = set()
                # Use XOR to toggle the lights - this handles cases where we
                # press a button twice. e.g. {1, 3} ^ {2, 3} = {1, 2}
                for button in attempt:
                    lights ^= button
                # The first match is guaranteed to be the optimal for that
                # machine.
                if lights == target:
                    total_presses += num_buttons
                    found = True
                    break

            if found:
                break

    return total_presses


def part_two(input_file: str): ...


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
