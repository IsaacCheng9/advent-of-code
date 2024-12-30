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
    def get_perimeter(region: set[tuple[int, int]]) -> int:
        perimeter = 0

        # Check each plot in the region.
        for row, col in region:
            # Start with 4 edges for the region, then subtract 1 for each
            # edge that is shared with another cell in the region.
            perimeter += 4
            for row_diff, col_diff in directions:
                neighbour_row = row + row_diff
                neighbour_col = col + col_diff
                if (neighbour_row, neighbour_col) in region:
                    perimeter -= 1

        return perimeter

    grid = parse_2d_grid_strs(file_name)
    rows = len(grid)
    cols = len(grid[0])
    directions = ((-1, 0), (0, -1), (0, 1), (1, 0))
    regions = []
    seen = set()

    # Find all regions using flood fill.
    for row in range(rows):
        for col in range(cols):
            # Skip cells that we've already processed.
            if (row, col) in seen:
                continue

            # Start a new region with the current cell.
            seen.add((row, col))
            region = {(row, col)}
            queue = deque([(row, col)])

            # Perform BFS to find all connected plots of the same type.
            while queue:
                cur_row, cur_col = queue.popleft()
                for row_diff, col_diff in directions:
                    new_row = cur_row + row_diff
                    new_col = cur_col + col_diff
                    # Skip if we're out of bounds, there's a different plot
                    # type, or we've already processed this cell.
                    if (
                        new_row not in range(rows)
                        or new_col not in range(cols)
                        or grid[new_row][new_col] != grid[row][col]
                        or (new_row, new_col) in region
                    ):
                        continue
                    # Mark the new cell as part of the region and add it to the
                    # deque so we can process its neighbours.
                    region.add((new_row, new_col))
                    queue.append((new_row, new_col))

            # Mark all positions in the region as seen and add it to the list
            # of regions.
            seen |= region
            regions.append(region)

    # The sum for each region is the area (number of cells) * the perimeter.
    return sum(len(region) * get_perimeter(region) for region in regions)


def part_two(file_name: str) -> int:
    def get_num_sides(region: set[tuple[int, int]]) -> int:
        # Store the edges and their directions.
        # (row, col): (x_direction_vector, y_direction_vector)
        edge_vectors = {}
        # Find all external edges.
        for row, col in region:
            for row_diff, col_diff in directions:
                new_row = row + row_diff
                new_col = col + col_diff
                # Skip shared edges, as they aren't external.
                if (new_row, new_col) in region:
                    continue

                # Calculate the midpoint of the edge between the two cells.
                edge_midpoint_row = (row + new_row) / 2
                edge_midpoint_col = (col + new_col) / 2
                direction_vector = (edge_midpoint_row - row, edge_midpoint_col - col)
                edge_vectors[(edge_midpoint_row, edge_midpoint_col)] = direction_vector

        num_sides = 0
        seen = set()
        for edge, vector in edge_vectors.items():
            if edge in seen:
                continue
            seen.add(edge)
            num_sides += 1
            edge_row, edge_col = edge

            # Process vertical edges (column remains the same).
            # If we have a whole number row, we're processing a vertical
            # edge because the midpoint calculation showed no change in row.
            if edge_row % 1 == 0:
                # Look for connected vertical edges above and below.
                for row_diff in (-1, 1):
                    new_row = edge_row + row_diff
                    # Continue finding connected edges vertically.
                    while edge_vectors.get((new_row, edge_col)) == vector:
                        seen.add(((new_row, edge_col)))
                        new_row += row_diff

            # Process horizontal edges (row remains the same).
            # If we have a whole number column, we're processing a horizontal
            # edge because the midpoint calculation showed no change in column.
            else:
                # Look for connected horizontal edges to the left and right.
                for col_diff in (-1, 1):
                    new_col = edge_col + col_diff
                    # Continue finding connected edges horizontally.
                    while edge_vectors.get((edge_row, new_col)) == vector:
                        seen.add(((edge_row, new_col)))
                        new_col += col_diff

        return num_sides

    grid = parse_2d_grid_strs(file_name)
    rows = len(grid)
    cols = len(grid[0])
    directions = ((-1, 0), (0, -1), (0, 1), (1, 0))
    regions = []
    seen = set()

    # Find all regions using flood fill.
    for row in range(rows):
        for col in range(cols):
            # Skip cells that we've already processed.
            if (row, col) in seen:
                continue

            # Start a new region with the current cell.
            seen.add((row, col))
            region = {(row, col)}
            queue = deque([(row, col)])

            # Perform BFS to find all connected plots of the same type.
            while queue:
                cur_row, cur_col = queue.popleft()
                for row_diff, col_diff in directions:
                    new_row = cur_row + row_diff
                    new_col = cur_col + col_diff
                    # Skip if we're out of bounds, there's a different plot
                    # type, or we've already processed this cell.
                    if (
                        new_row not in range(rows)
                        or new_col not in range(cols)
                        or grid[new_row][new_col] != grid[row][col]
                        or (new_row, new_col) in region
                    ):
                        continue
                    # Mark the new cell as part of the region and add it to the
                    # deque so we can process its neighbours.
                    region.add((new_row, new_col))
                    queue.append((new_row, new_col))

            # Mark all positions in the region as seen and add it to the list
            # of regions.
            seen |= region
            regions.append(region)

    # The sum for each region is the area (number of cells) * the number of
    # sides.
    return sum(len(region) * get_num_sides(region) for region in regions)


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
