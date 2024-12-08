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
    run_with_timing,
    parse_input_without_trailing_and_leading_whitespace,
    parse_lines,
    parse_ints,
    parse_2d_grid,
    calculate_manhattan_distance,
)


def part_one(file_name: str) -> int:
    grid = parse_2d_grid(file_name)
    rows = len(grid)
    cols = len(grid[0])

    # Find the starting position.
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == "^":
                break
        # Runs if the for loop didn't break, so we continue to the next cell.
        else:
            continue
        # If we break in the for loop, we'll break here so we stop iterating.
        break

    # We move up initially.
    row_diff = -1
    col_diff = 0
    # Mark seen cells in a hash set so we can track the distinct positions.
    distinct_positions = set()

    while True:
        distinct_positions.add((row, col))
        new_row = row + row_diff
        new_col = col + col_diff
        # Continue moving until we go out of bounds.
        if new_row not in range(rows) or new_col not in range(cols):
            break

        # If we bump into an obstruction, turn right by swapping the row and
        # column differences, and applying a negative sign to the new column
        # difference.
        if grid[new_row][new_col] == "#":
            row_diff, col_diff = col_diff, -row_diff
        # Otherwise, continue moving in the same direction.
        else:
            row += row_diff
            col += col_diff

    return len(distinct_positions)


def part_two(file_name: str) -> int:
    def new_obstruction_creates_a_loop(grid, row, col):
        row_diff = -1
        col_diff = 0
        seen = set()

        while True:
            new_row = row + row_diff
            new_col = col + col_diff
            seen.add((row, col, row_diff, col_diff))
            if new_row not in range(rows) or new_col not in range(cols):
                return False

            # If we bump into an obstruction, turn right by swapping the row and
            # column differences, and applying a negative sign to the new column
            # difference.
            if grid[new_row][new_col] == "#":
                row_diff, col_diff = col_diff, -row_diff
            # Otherwise, continue moving in the same direction.
            else:
                row += row_diff
                col += col_diff

            # If we get into the same position and are facing the same
            # direction, then we've created a loop.
            if (row, col, row_diff, col_diff) in seen:
                return True

    grid = parse_2d_grid(file_name)
    rows = len(grid)
    cols = len(grid[0])

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == "^":
                break
        # Runs if the for loop didn't break, so we continue to the next cell.
        else:
            continue
        # If we break in the for loop, we'll break here so we stop iterating.
        break

    new_obstruction_position_count = 0

    # Try creating the new obstruction in each cell and increment the count if
    # it creates a loop via backtracking.
    for new_obstruction_row in range(rows):
        for new_obstruction_col in range(cols):
            # If it's not an empty cell, we can't place an obstruction here.
            if grid[new_obstruction_row][new_obstruction_col] != ".":
                continue

            # Place the obstruction and check if it creates a loop.
            grid[new_obstruction_row][new_obstruction_col] = "#"
            if new_obstruction_creates_a_loop(grid, row, col):
                new_obstruction_position_count += 1
            # Remove the obstruction so we can try placing it on a different
            # cell in the next iteration.
            grid[new_obstruction_row][new_obstruction_col] = "."

    return new_obstruction_position_count


if __name__ == "__main__":
    day_path = Path(__file__).parent
    input_path = day_path / "input.txt"

    print("\n--- Part One ---")
    answer1, duration1 = run_with_timing(part_one, str(input_path))
    print(f"Answer: {answer1}")
    print(f"Time: {duration1:.4f} seconds")

    # !IMPORTANT: Runs quite slowly due to the backtracking approach.
    print("\n--- Part Two ---")
    answer2, duration2 = run_with_timing(part_two, str(input_path))
    print(f"Answer: {answer2}")
    print(f"Time: {duration2:.4f} seconds")

    print(f"\nTotal time: {duration1 + duration2:.4f} seconds")