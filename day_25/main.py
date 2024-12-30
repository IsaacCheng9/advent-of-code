import heapq  # noqa
import os  # noqa
from pathlib import Path
import sys  # noqa
import re  # noqa
import math  # noqa
import fileinput  # noqa
from string import ascii_uppercase, ascii_lowercase  # noqa
from collections import Counter, defaultdict, deque, namedtuple  # noqa
from itertools import (  # noqa
    count,  # noqa
    product,  # noqa
    permutations,  # noqa
    combinations,  # noqa
    combinations_with_replacement,  # noqa
)

# Add the parent directory to the PYTHONPATH.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.utils import (  # noqa
    execute_with_runtime,
    parse_input,
    parse_lines,
    parse_list_of_ints,
    parse_2d_grid_strs,
    calculate_manhattan_distance,
)


def part_one(input_file: str) -> int:
    input_data = parse_input(input_file)
    # Split the input into blocks, where each block represents a lock or key.
    blocks = input_data.split("\n\n")
    locks = []
    keys = []

    for block in blocks:
        # Convert each grid into a 2D grid and transpose it to work with
        # columns via zip(*lines). This allows us to use the built-in count()
        # method to efficiently count the number of #s in each column, rather
        # than manually iterating through rows to count vertically.
        grid = list(zip(*block.splitlines()))
        # Locks have a # in the top-left corner, while keys have a ".".
        # Count the number of #s in each column and subtract 1 to get
        # pin heights.
        if grid[0][0] == "#":
            locks.append([row.count("#") - 1 for row in grid])
        else:
            keys.append([row.count("#") - 1 for row in grid])

    # Count the total number of valid pairs of locks and keys.
    total_valid_pairs = 0
    for lock in locks:
        for key in keys:
            # For each pin position, the lock pin height and key tooth height
            # must not exceed 5, as it's a 5-pin lock.
            if all(x + y <= 5 for x, y in zip(lock, key)):
                total_valid_pairs += 1

    return total_valid_pairs


if __name__ == "__main__":
    day_path = Path(__file__).parent
    input_path = day_path / "input.txt"

    print("\n--- Part One ---")
    answer1, duration1 = execute_with_runtime(part_one, str(input_path))
    print(f"Answer: {answer1}")
    print(f"Runtime: {duration1:.4f} milliseconds")

    print(f"\nTotal runtime: {duration1:.4f} milliseconds")
