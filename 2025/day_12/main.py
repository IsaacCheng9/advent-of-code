import fileinput  # noqa
import heapq  # noqa
import io  # noqa
import math  # noqa
import numpy as np  # noqa
import os  # noqa
import pandas as pd  ## noqa
import re  # noqa
import sys  # noqa
from collections import Counter, defaultdict, deque, namedtuple  # noqa
from functools import cache, lru_cache  # noqa
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


def part_one(file_path: str):
    data = parse_input(file_path)
    *shapes, regions = data.split("\n\n")
    # Count '#' cells in each shape to get their areas.
    shape_sizes = [sum(c == "#" for c in shape) for shape in shapes]
    valid_count = 0

    for region in regions.split("\n"):
        dimensions, counts = region.split(": ")
        width, height = map(int, dimensions.split("x"))
        counts = list(map(int, counts.split()))

        area = width * height
        area_required = sum(num * size for num, size in zip(counts, shape_sizes))
        # A region is valid if it can fit all the requested shapes. Note that
        # this is a necessary but not sufficient condition - shapes may not
        # physically fit due to their geometry, but the problem doesn't ask
        # us to actually place the shapes.
        if area >= area_required:
            valid_count += 1

    return valid_count


if __name__ == "__main__":
    day_path = Path(__file__).parent
    input_path = day_path / "input.txt"

    print("\n--- Part One ---")
    answer1, duration1 = execute_with_runtime(part_one, str(input_path))
    print(f"Answer: {answer1}")
    print(f"Runtime: {duration1:.4f} milliseconds")
