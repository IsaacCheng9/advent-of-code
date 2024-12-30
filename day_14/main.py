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
    input_data = parse_lines(file_name)
    GRID_ROWS = 103
    GRID_COLS = 101
    MIDDLE_ROW = (GRID_ROWS - 1) // 2
    MIDDLE_COL = (GRID_COLS - 1) // 2

    # Store the initial positions and velocities of the robots.
    # [(pos_col, pos_row, velocity_col, velocity_row), ...]
    robots_before_sim = []
    for line in input_data:
        pos, velocity = line.split()
        pos_col, pos_row = map(int, pos[2:].split(","))
        velocity_col, velocity_row = map(int, velocity[2:].split(","))
        robots_before_sim.append((pos_col, pos_row, velocity_col, velocity_row))

    # Simulate 100 moves for each robot.
    robots_after_sim = []
    for pos_col, pos_row, velocity_col, velocity_row in robots_before_sim:
        robots_after_sim.append(
            (
                # Use modulo to wrap around the grid.
                (pos_col + velocity_col * 100) % GRID_COLS,
                (pos_row + velocity_row * 100) % GRID_ROWS,
            )
        )

    # Get the positions of each robot after 100 moves.
    top_left = top_right = bottom_left = bottom_right = 0
    for pos_col, pos_row in robots_after_sim:
        # Robots in the middle row or column aren't counted as relevant.
        if pos_col == MIDDLE_COL or pos_row == MIDDLE_ROW:
            continue
        # Count the robots in the four quadrants.
        if pos_col < MIDDLE_COL:
            if pos_row < MIDDLE_ROW:
                top_left += 1
            else:
                bottom_left += 1
        else:
            if pos_row < MIDDLE_ROW:
                top_right += 1
            else:
                bottom_right += 1

    # The result is the multiplication of the count in each quadrant.
    return top_left * bottom_left * top_right * bottom_right


def part_two(file_name: str) -> int:
    input_data = parse_lines(file_name)
    ROWS = 103
    COLS = 101
    MIDDLE_ROW = (ROWS - 1) // 2
    MIDDLE_COL = (COLS - 1) // 2

    # Store the initial positions and velocities of the robots.
    # [(pos_col, pos_row, velocity_col, velocity_row), ...]
    robots_before_sim = []
    for line in input_data:
        pos, velocity = line.split()
        pos_col, pos_row = map(int, pos[2:].split(","))
        velocity_col, velocity_row = map(int, velocity[2:].split(","))
        robots_before_sim.append((pos_col, pos_row, velocity_col, velocity_row))

    # Simulate the robots after each move and track the minimum safety factor.
    min_safety_factor = float("inf")
    min_safety_factor_time = 0
    # Try ROWS * COLS moves, as after this time the robots will be back to
    # their initial positions due to wrapping around the grid.
    for second in range(ROWS * COLS):
        robots_after_sim = []
        for pos_col, pos_row, velocity_col, velocity_row in robots_before_sim:
            robots_after_sim.append(
                (
                    # Use modulo to wrap around the grid.
                    (pos_col + (velocity_col * second)) % COLS,
                    (pos_row + (velocity_row * second)) % ROWS,
                )
            )

        # Get the positions of each robot after this move.
        top_left = top_right = bottom_left = bottom_right = 0
        for pos_col, pos_row in robots_after_sim:
            # Robots in the middle row or column aren't counted as relevant.
            if pos_col == MIDDLE_COL or pos_row == MIDDLE_ROW:
                continue
            # Count the robots in the four quadrants.
            if pos_col < MIDDLE_COL:
                if pos_row < MIDDLE_ROW:
                    top_left += 1
                else:
                    bottom_left += 1
            else:
                if pos_row < MIDDLE_ROW:
                    top_right += 1
                else:
                    bottom_right += 1

        # The result is the multiplication of the count in each quadrant.
        safety_factor = top_left * bottom_left * top_right * bottom_right
        if safety_factor < min_safety_factor:
            min_safety_factor = safety_factor
            min_safety_factor_time = second

    return min_safety_factor_time


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
