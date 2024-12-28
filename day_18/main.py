"""
Advent of Code solution template with enhanced utilities.
"""

import heapq  # NOQA
import os  # NOQA
from pathlib import Path
import sys  # NOQA
import re  # NOQA
import math  # NOQA
import fileinput  # NOQA
from bisect import bisect_left  # NOQA
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
    # Simulate the first 1024 bytes falling onto the memory space represented
    # by a 2D grid with coordinates 0 to 70.
    GRID_SIZE = 70
    NUM_BYTES = 1024
    input_data = parse_lines(file_name)
    # Create a list of tuples from the input lines.
    coordinates = [tuple(map(int, line.split(","))) for line in input_data]
    # Bytes can move left, up, down, or right.
    directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]

    # Create a 2D grid with dimensions (GRID_SIZE + 1) * (GRID_SIZE + 1).
    # 0s represent safe spaces, and 1s represent corrupted memory.
    grid = [[0] * (GRID_SIZE + 1) for _ in range(GRID_SIZE + 1)]
    # Mark corrupted memory locations in the grid. The coordinates are in
    # (col, row) format, so reverse them for grid indexing. Take only the first
    # NUM_BYTES elements from the coordinates list so that we can simulate
    # that number of bytes falling.
    for col, row in coordinates[:NUM_BYTES]:
        grid[row][col] = 1

    # We start at the top-left of the grid.
    queue = deque([(0, 0, 0)])
    # Track seen positions to avoid cycles.
    seen = {(0, 0)}

    # Perform BFS to find the shortest path to the exit.
    while queue:
        row, col, distance = queue.popleft()
        # Check all four directions.
        for row_diff, col_diff in directions:
            new_row = row + row_diff
            new_col = col + col_diff
            # Skip cells that are out of bounds, hit corrupted memory, or have
            # already been visited.
            if (
                new_row not in range(GRID_SIZE + 1)
                or new_col not in range(GRID_SIZE + 1)
                or grid[new_row][new_col] == 1
                or (new_row, new_col) in seen
            ):
                continue

            # If we've reached the exit position, return the distance.
            if new_row == new_col == GRID_SIZE:
                return distance + 1
            # Otherwise, mark the current position as seen and explore its
            # neighbours in a later BFS iteration.
            seen.add((new_row, new_col))
            queue.append((new_row, new_col, distance + 1))

    raise ValueError("No path to the exit found.")


def part_two(file_name: str) -> str:
    def has_path_to_exit(byte_count):
        # Create a 2D grid with dimensions (GRID_SIZE + 1) * (GRID_SIZE + 1).
        # 0s represent safe spaces, and 1s represent corrupted memory.
        grid = [[0] * (GRID_SIZE + 1) for _ in range(GRID_SIZE + 1)]
        # Mark corrupted memory locations in the grid. The coordinates are in
        # (col, row) format, so reverse them for grid indexing. Take only the
        # first byte_count elements from the coordinates list so that we can
        # simulate that number of bytes falling.
        for col, row in coordinates[:byte_count]:
            grid[row][col] = 1

        # We start at the top-left of the grid.
        queue = deque([(0, 0)])
        # Track seen positions to avoid cycles.
        seen = {(0, 0)}

        while queue:
            row, col = queue.popleft()
            # Check all four directions.
            for row_diff, col_diff in directions:
                new_row = row + row_diff
                new_col = col + col_diff
                # Skip cells that are out of bounds, hit corrupted memory, or have
                # already been visited.
                if (
                    new_row not in range(GRID_SIZE + 1)
                    or new_col not in range(GRID_SIZE + 1)
                    or grid[new_row][new_col] == 1
                    or (new_row, new_col) in seen
                ):
                    continue

                # If we've reached the exit position, a path exists.
                if new_row == new_col == GRID_SIZE:
                    return True
                # Otherwise, mark the current position as seen and explore its
                # neighbours in a later BFS iteration.
                seen.add((new_row, new_col))
                queue.append((new_row, new_col))

        # If we've explored all possible paths, there's no path to the exit.
        return False

    GRID_SIZE = 70
    input_data = parse_lines(file_name)
    # Create a list of tuples from the input lines.
    coordinates = [tuple(map(int, line.split(","))) for line in input_data]
    # Bytes can move left, up, down, or right.
    directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]

    # Perform binary search to find the first byte that blocks the path.
    # This works because once a path is blocked, it remains blocked when more
    # bytes fall, creating a clear division point we can search for.
    blocking_byte_index = bisect_left(
        range(len(coordinates)), True, key=lambda x: not has_path_to_exit(x + 1)
    )

    # Return a comma-separated string of coordinates of the first byte that
    # blocks the path.
    return ",".join(map(str, coordinates[blocking_byte_index]))


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
