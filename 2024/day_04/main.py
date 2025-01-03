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
    grid = parse_2d_grid_strs(input_file)
    pattern = "XMAS"
    rows = len(grid)
    cols = len(grid[0])
    res = 0

    # Check all 8 directions adjacent and diagonal.
    directions = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]

    # Try each starting position
    for row in range(rows):
        for col in range(cols):
            for row_diff, col_diff in directions:
                # Check if pattern fits in this direction from this position
                if (
                    0 <= row + row_diff * (len(pattern) - 1) < rows
                    and 0 <= col + col_diff * (len(pattern) - 1) < cols
                ):
                    # Check if pattern matches in this direction
                    matches = True
                    for i in range(len(pattern)):
                        if grid[row + row_diff * i][col + col_diff * i] != pattern[i]:
                            matches = False
                            break
                    if matches:
                        res += 1

    return res


def part_two(input_file: str) -> int:
    def check_x_mas(grid, x, y):
        valid_patterns = {"MAS", "SAM"}
        # Check bounds - need 3x3 space for the X pattern
        if x < 1 or x >= rows - 1 or y < 1 or y >= cols - 1:
            return False
        # Middle must be 'A'
        if grid[x][y] != "A":
            return False

        # Check the four possible combinations:
        # 1. Both diagonals MAS
        # 2. Upper-left to lower-right MAS, other SAM
        # 3. Upper-left to lower-right SAM, other MAS
        # 4. Both diagonals SAM
        upper_left_to_lower_right = [
            grid[x - 1][y - 1],
            grid[x][y],
            grid[x + 1][y + 1],
        ]
        upper_right_to_lower_left = [
            grid[x - 1][y + 1],
            grid[x][y],
            grid[x + 1][y - 1],
        ]

        # Convert to strings for easier comparison
        diag1 = "".join(upper_left_to_lower_right)
        diag2 = "".join(upper_right_to_lower_left)

        # Check if both diagonals are valid
        return diag1 in valid_patterns and diag2 in valid_patterns

    grid = parse_2d_grid_strs(input_file)
    rows = len(grid)
    cols = len(grid[0])
    res = 0

    # Check each possible middle position
    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            if check_x_mas(grid, row, col):
                res += 1

    return res


if __name__ == "__main__":
    day_path = Path(__file__).parent
    input_path = day_path / "input.txt"

    print("--- Part One ---")
    answer1, duration1 = execute_with_runtime(part_one, str(input_path))
    print(f"Answer: {answer1}")
    print(f"Runtime: {duration1:.4f} milliseconds")

    print("\n--- Part Two ---")
    answer2, duration2 = execute_with_runtime(part_two, str(input_path))
    print(f"Answer: {answer2}")
    print(f"Runtime: {duration2:.4f} milliseconds")

    print(f"\nTotal runtime: {duration1 + duration2:.4f} milliseconds")
