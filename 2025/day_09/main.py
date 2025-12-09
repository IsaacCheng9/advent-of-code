import fileinput  # noqa
import heapq  # noqa
import math  # noqa
import os  # noqa
import re  # noqa
import sys  # noqa
from collections import Counter, defaultdict, deque, namedtuple  # noqa
from functools import cache  # noqa
from itertools import (  # noqa
    combinations,
    combinations_with_replacement,
    count,
    permutations,
    product,
)
from bisect import bisect_left, bisect_right  # noqa
from math import gcd, lcm  # noqa
from pathlib import Path  # noqa
from string import ascii_lowercase, ascii_uppercase  # noqa
from shapely.geometry.polygon import Polygon

# Add the parent directory to the PYTHONPATH.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.utils import (  # noqa
    calculate_manhattan_distance,
    execute_with_runtime,
    parse_2d_grid_strs,
    parse_input,
    parse_lines,
    parse_list_of_ints,
)


def part_one(input_file: str):
    lines = parse_lines(input_file)

    # Parse coordinates.
    tiles = []
    for line in lines:
        x, y = map(int, line.split(","))
        tiles.append((x, y))

    # Find the maximum area by trying all pairs.
    max_area = 0
    for index1 in range(len(tiles)):
        for index2 in range(index1 + 1, len(tiles)):
            x1, y1 = tiles[index1]
            x2, y2 = tiles[index2]
            # Add 1 to both dimensions to count tiles inclusively.
            area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            max_area = max(max_area, area)

    return max_area


def part_two(input_file: str):
    def calculate_area(x1: int, y1: int, x2: int, y2: int) -> int:
        width = abs(int(x2) - int(x1)) + 1
        height = abs(int(y2) - int(y1)) + 1
        return width * height

    def create_rectangle(x1: int, y1: int, x2: int, y2: int) -> Polygon:
        return Polygon([(x1, y1), (x1, y2), (x2, y2), (x2, y1)])

    # Parse coordinates forming the polygon vertices.
    data = parse_lines(input_file)
    vertices = []
    for line in data:
        x, y = map(int, line.split(","))
        vertices.append((x, y))

    # Create the bounding polygon from the ordered vertices.
    bounding_polygon = Polygon(vertices)
    max_area = 0

    # Try all pairs of vertices as opposite corners of a rectangle.
    for coord1 in vertices:
        for coord2 in vertices:
            rectangle = create_rectangle(coord1[0], coord1[1], coord2[0], coord2[1])
            # Check if the rectangle is fully inside the polygon.
            if bounding_polygon.contains(rectangle):
                area = calculate_area(coord1[0], coord1[1], coord2[0], coord2[1])
                max_area = max(max_area, area)

    return max_area


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
