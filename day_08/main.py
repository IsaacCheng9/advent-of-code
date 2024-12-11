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
    grid = parse_2d_grid_strs(file_name)
    rows = len(grid)
    cols = len(grid[0])

    # Group antennas by their frequency (char) and store a list of their
    # positions.
    antennas = defaultdict(list)
    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            # If it's not an empty space, it's an antenna.
            if char != ".":
                antennas[char].append((r, c))

    # Store unique antinode positions.
    antinodes = set()
    for array in antennas.values():
        # Check every pair of antennas.
        for i in range(len(array)):
            for j in range(i + 1, len(array)):
                r1, c1 = array[i]
                r2, c2 = array[j]
                # Calculate both possible antinode positions, using:
                # 1) First antenna as the middle point
                # 2) Second antenna as the middle point
                antinodes.add((2 * r1 - r2, 2 * c1 - c2))
                antinodes.add((2 * r2 - r1, 2 * c2 - c1))

    # Filter antinodes that are out of bounds.
    valid_antinodes = {
        (row, col)
        for row, col in antinodes
        if row in range(rows) and col in range(cols)
    }
    return len(valid_antinodes)


def part_two(file_name: str) -> int:
    grid = parse_2d_grid_strs(file_name)
    rows = len(grid)
    cols = len(grid[0])

    # Group antennas by their frequency (char) and store a list of their
    # positions.
    antennas = defaultdict(list)
    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            # If it's not an empty space, it's an antenna.
            if char != ".":
                antennas[char].append((r, c))

    # Store unique antinode positions.
    antinodes = set()
    for array in antennas.values():
        # For each frequency, trace lines from each antenna to every other
        # antenna. Unlike part 1, we need to trace from both a -> b and
        # b -> a because we're marking all points along the line as antinodes,
        # and the walls can block each trace differently.
        for i in range(len(array)):
            for j in range(len(array)):
                # Skip pairs with itself to avoid an infinite loop caused by
                # the row_diff and col_diff being 0.
                if i == j:
                    continue

                # Get the starting and ending antenna positions.
                r1, c1 = array[i]
                r2, c2 = array[j]
                # Calculate the direction vector to trace the line between the
                # two antennas.
                row_diff = r2 - r1
                col_diff = c2 - c1

                # Start at the first antenna and keep stepping by the direction
                # vector - mark each position as an antinode until we hit a
                # wall or go out of bounds.
                cur_row = r1
                cur_col = c1
                while cur_row in range(rows) and cur_col in range(cols):
                    if grid[cur_row][cur_col] == "#":
                        break
                    antinodes.add((cur_row, cur_col))
                    cur_row += row_diff
                    cur_col += col_diff

    # Filter antinodes that are out of bounds.
    valid_antinodes = {
        (row, col)
        for row, col in antinodes
        if row in range(rows) and col in range(cols)
    }
    return len(valid_antinodes)


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
