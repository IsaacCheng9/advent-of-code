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


def part_one(file_name: str) -> int:
    input_data = parse_input(file_name)
    raw_grid, robot_moves = input_data.split("\n\n")
    grid = [list(line) for line in raw_grid.splitlines()]
    ROWS = len(grid)
    COLS = len(grid[0])
    MOVES_MAP = {
        "^": (-1, 0),  # Up
        "v": (1, 0),  # Down
        "<": (0, -1),  # Left
        ">": (0, 1),  # Right
    }
    # Combine all movement instructions into a single string for easier
    # processing.
    robot_moves = "".join(robot_moves.splitlines())

    # Get the initial position of the robot (@).
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == "@":
                break
        else:
            continue
        break

    # Process each move.
    for move in robot_moves:
        # Translate the character into the row and column differences.
        row_diff, col_diff = MOVES_MAP[move]
        # Track positions that need to be updated (robot and boxes).
        affected_positions = [(row, col)]
        cur_row = row
        cur_col = col
        # Track whether we can continue moving in the movement direction.
        movement_allowed = True

        # Scan ahead in the movement direction to check if movement is
        # possible and identify the boxes that would be affected.
        while True:
            cur_row += row_diff
            cur_col += col_diff
            cell = grid[cur_row][cur_col]
            # If we hit a wall, stop moving.
            if cell == "#":
                movement_allowed = False
                break
            # If we hit a box, add it to the list of affected positions and
            # continue moving in the same direction.
            elif cell == "O":
                affected_positions.append((cur_row, cur_col))
            # If we found an empty space, stop moving.
            elif cell == ".":
                break

        # If we would hit a wall, nothing moves.
        if not movement_allowed:
            continue

        # Clear the robot's current position.
        grid[row][col] = "."
        # Move the robot to the new position.
        grid[row + row_diff][col + col_diff] = "@"
        # Clear the old positions of all boxes. Skip the 0th index as this
        # contains the robot's position.
        for box_row, box_col in affected_positions[1:]:
            grid[box_row + row_diff][box_col + col_diff] = "O"

        # Update the robot's position for the next movement.
        row += row_diff
        col += col_diff

    return sum(
        100 * row + col
        for row in range(ROWS)
        for col in range(COLS)
        if grid[row][col] == "O"
    )


def part_two(file_name: str) -> int:
    input_data = parse_input(file_name)
    raw_grid, robot_moves = input_data.split("\n\n")
    # Create the expanded grid where each cell becomes two cells wide.
    cell_expansion_map = {
        "#": "##",
        "O": "[]",
        ".": "..",
        "@": "@.",
    }
    grid = [
        list("".join(cell_expansion_map[char] for char in line))
        for line in raw_grid.splitlines()
    ]
    ROWS = len(grid)
    COLS = len(grid[0])
    MOVES_MAP = {
        "^": (-1, 0),  # Up
        "v": (1, 0),  # Down
        "<": (0, -1),  # Left
        ">": (0, 1),  # Right
    }
    # Combine all movement instructions into a single string for easier
    # processing.
    robot_moves = "".join(robot_moves.splitlines())

    # Get the initial position of the robot.
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == "@":
                break
        else:
            continue
        break

    for move in robot_moves:
        # Translate the character into the row and column differences.
        row_diff, col_diff = MOVES_MAP[move]
        # Track positions that need to be updated (robot and boxes).
        affected_positions = [(row, col)]
        # Track whether we can continue moving in the movement direction.
        movement_allowed = True

        # For each position marked as affected, check what's in the movement
        # direction so we can handle chain reactions where one box pushes
        # another box.
        for cur_row, cur_col in affected_positions:
            next_row = cur_row + row_diff
            next_col = cur_col + col_diff
            # Skip if the position is already marked as affected.
            if (next_row, next_col) in affected_positions:
                continue
            cell = grid[next_row][next_col]

            # If we hit a wall, stop moving.
            if cell == "#":
                movement_allowed = False
                break
            # If we hit the left side of a box, track both halves.
            elif cell == "[":
                affected_positions.append((next_row, next_col))
                affected_positions.append((next_row, next_col + 1))
            # If we hit the right side of a box, track both halves.
            elif cell == "]":
                affected_positions.append((next_row, next_col))
                affected_positions.append((next_row, next_col - 1))

        # If any piece would hit a wall, nothing moves.
        if not movement_allowed:
            continue

        # Make a copy of the grid to reference the original box characters.
        grid_copy = [list(row) for row in grid]

        # Clear the robot's current position.
        grid[row][col] = "."
        # Move the robot to the new position.
        grid[row + row_diff][col + col_diff] = "@"
        # Clear the old positions of all boxes. Skip the 0th index as this
        # contains the robot's position.
        for box_row, box_col in affected_positions[1:]:
            grid[box_row][box_col] = "."
        # Move all boxes to their new positions, preserving their original
        # characters.
        for box_row, box_col in affected_positions[1:]:
            grid[box_row + row_diff][box_col + col_diff] = grid_copy[box_row][box_col]

        # Update the robot's position for the next movement.
        row += row_diff
        col += col_diff

    # Sum the GPS coordinates using only the left half of each box.
    return sum(
        100 * row + col
        for row in range(ROWS)
        for col in range(COLS)
        if grid[row][col] == "["
    )


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
