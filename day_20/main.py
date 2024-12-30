import heapq  # NOQA
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
from urllib import parse

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


def part_one(input_file: str) -> int:
    grid = parse_2d_grid_strs(input_file)
    ROWS = len(grid)
    COLS = len(grid[0])
    MOVES = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Find the start position.
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == "S":
                break
        else:
            continue
        break

    # Count the number of picoseconds from the start position in a 2D array.
    picosecond_counts = [[-1] * COLS for _ in range(ROWS)]
    picosecond_counts[row][col] = 0

    # Use a modified BFS that follows a single path to the end position,
    # recording the minimum number of picoseconds to reach each cell.
    while grid[row][col] != "E":
        # Move to each neighbouring cell and update the picoseconds.
        for row_diff, col_diff in MOVES:
            new_row = row + row_diff
            new_col = col + col_diff

            # Skip the neighbouring cell if it's out of bounds, a wall, or it
            # has already been visited earlier in the BFS (as this would create
            # a longer path).
            if (
                new_row not in range(ROWS)
                or new_col not in range(COLS)
                or grid[new_row][new_col] == "#"
                or picosecond_counts[new_row][new_col] != -1
            ):
                continue

            # Update the picoseconds and move to the next cell.
            picosecond_counts[new_row][new_col] = picosecond_counts[row][col] + 1
            row = new_row
            col = new_col

    # Count the number of cheats that would save at least 100 piseconds.
    num_cheats = 0
    for row in range(ROWS):
        for col in range(COLS):
            # Skip the cell if it's a wall.
            if grid[row][col] == "#":
                continue

            # Try each cheat, but only move 'forward' from our current position
            # to avoid counting each cheat twice, as cheat A -> B is equivalent
            # to cheat B -> A.
            for new_row, new_col in [
                (row + 2, col),  # Two down
                (row + 1, col + 1),  # Down-right
                (row, col + 2),  # Two right
                (row - 1, col + 1),  # Up-right
            ]:
                # Skip the neighbouring cell if it's out of bounds or a wall.
                if (
                    new_row not in range(ROWS)
                    or new_col not in range(COLS)
                    or grid[new_row][new_col] == "#"
                ):
                    continue

                # Check if the cheat would save at least 100 piseconds. The
                # difference between the normal path length and cheat length
                # (2) must be at least 102 to save 100 picoseconds overall.
                if (
                    abs(
                        picosecond_counts[row][col]
                        - picosecond_counts[new_row][new_col]
                    )
                    >= 102
                ):
                    num_cheats += 1

    return num_cheats


def part_two(input_file: str) -> int:
    grid = parse_2d_grid_strs(input_file)
    ROWS = len(grid)
    COLS = len(grid[0])
    MOVES = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Find the start position.
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == "S":
                break
        else:
            continue
        break

    # Count the number of picoseconds from the start position in a 2D array.
    picosecond_counts = [[-1] * COLS for _ in range(ROWS)]
    picosecond_counts[row][col] = 0

    # Use BFS to find the shortest path to the end position.
    while grid[row][col] != "E":
        # Move to each neighbouring cell and update the picoseconds.
        for row_diff, col_diff in MOVES:
            new_row = row + row_diff
            new_col = col + col_diff

            # Skip the neighbouring cell if it's out of bounds, a wall, or it
            # has already been visited earlier in the BFS (as this would create
            # a longer path).
            if (
                new_row not in range(ROWS)
                or new_col not in range(COLS)
                or grid[new_row][new_col] == "#"
                or picosecond_counts[new_row][new_col] != -1
            ):
                continue

            # Update the picoseconds and move to the next cell.
            picosecond_counts[new_row][new_col] = picosecond_counts[row][col] + 1
            row = new_row
            col = new_col

    # Count the number of cheats that would save at least 100 piseconds.
    num_cheats = 0
    for row in range(ROWS):
        for col in range(COLS):
            # Skip the cell if it's a wall.
            if grid[row][col] == "#":
                continue

            # Try each combination of row and column skips for the cheat length
            # from 2 to 21.
            for cheat_length in range(2, 21):
                for row_diff in range(cheat_length + 1):
                    col_diff = cheat_length - row_diff
                    # Try each row-column difference combination for the cheat.
                    for new_row, new_col in {
                        (row + row_diff, col + col_diff),  # Up-right
                        (row + row_diff, col - col_diff),  # Up-left
                        (row - row_diff, col + col_diff),  # Down-right
                        (row - row_diff, col - col_diff),  # Down-left
                    }:
                        # Skip the neighbouring cell if it's out of bounds or a
                        # wall.
                        if (
                            new_row not in range(ROWS)
                            or new_col not in range(COLS)
                            or grid[new_row][new_col] == "#"
                        ):
                            continue

                        # Check if the cheat saves at least 100 picoseconds. We
                        # must include the time taken to cheat in our
                        # calculation. We check the difference in this
                        # direction only, as the opposite direction will be
                        # checked when we process the other position.
                        if (
                            picosecond_counts[row][col]
                            - picosecond_counts[new_row][new_col]
                            >= 100 + cheat_length
                        ):
                            num_cheats += 1

    return num_cheats


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
