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
    parse_2d_grid_ints,
    calculate_manhattan_distance,
)


def part_one(file_name: str) -> int:
    def bfs(row, col):
        # Initialise the starting position and track seen positions so we don't
        # revisit them.
        queue = deque([(row, col)])
        seen = {(row, col)}
        num_summits = 0

        while queue:
            cur_row, cur_col = queue.popleft()

            # Try to move in all directions.
            for row_diff, col_diff in directions:
                new_row = cur_row + row_diff
                new_col = cur_col + col_diff
                # Ensure that the new position is within the grid, the new
                # position is one greater than the current position, and the
                # new position hasn't been visited before.
                if (
                    new_row not in range(rows)
                    or new_col not in range(cols)
                    or grid[new_row][new_col] != grid[cur_row][cur_col] + 1
                    or (new_row, new_col) in seen
                ):
                    continue

                # Mark the position as visited, and add it to the queue if it
                # isn't a summit to explore further.
                seen.add((new_row, new_col))
                if grid[new_row][new_col] == 9:
                    num_summits += 1
                else:
                    queue.append((new_row, new_col))

        return num_summits

    grid = parse_2d_grid_ints(file_name)
    rows = len(grid)
    cols = len(grid[0])
    directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]

    # Find all positions with a value of 0, as these are the trailheads that
    # represent our starting points.
    trailheads = [
        (row, col) for row in range(rows) for col in range(cols) if grid[row][col] == 0
    ]
    # Perform BFS from each trailhead and sum the number of summits found.
    total_summits = sum(bfs(row, col) for row, col in trailheads)

    return total_summits


def part_two(file_name: str) -> int:
    def bfs(row, col):
        # Initialise the starting position and track the number of trails that
        # lead to each summit.
        queue = deque([(row, col)])
        paths = {}
        paths[(row, col)] = 1
        num_trails = 0

        while queue:
            cur_row, cur_col = queue.popleft()
            # If we've reached a summit, increment the total by the number of
            # paths that led to it.
            if grid[cur_row][cur_col] == 9:
                num_trails += paths[(cur_row, cur_col)]

            # Try to move in all directions.
            for row_diff, col_diff in directions:
                new_row = cur_row + row_diff
                new_col = cur_col + col_diff
                # Ensure that the new position is within the grid and that
                # the new position is one greater than the current position.
                if (
                    new_row not in range(rows)
                    or new_col not in range(cols)
                    or grid[new_row][new_col] != grid[cur_row][cur_col] + 1
                ):
                    continue

                # Set the number of paths to this position equal to the number
                # of paths that led to our current position, as these paths
                # can now be extended to reach the new position.
                paths[(new_row, new_col)] = paths[(cur_row, cur_col)]
                queue.append((new_row, new_col))

        return num_trails

    grid = parse_2d_grid_ints(file_name)
    rows = len(grid)
    cols = len(grid[0])
    directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]

    # Find all positions with a value of 0, as these are the trailheads that
    # represent our starting points.
    trailheads = [
        (row, col) for row in range(rows) for col in range(cols) if grid[row][col] == 0
    ]
    # Perform BFS from each trailhead and sum the number of summits found.
    total_summits = sum(bfs(row, col) for row, col in trailheads)

    return total_summits


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
