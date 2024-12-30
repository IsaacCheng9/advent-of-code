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


def part_one(file_name: str) -> int:
    data = parse_input(file_name)
    res = 0

    # Find 1-3 digits separated by a comma.
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    for mul in re.findall(pattern, data):
        first, second = map(int, mul)
        res += first * second

    return res


def part_two(file_name: str) -> int:
    data = parse_input(file_name)
    res = 0

    # 'mul' instructions are enabled at the start.
    mul_enabled = True
    # Match either the 'mul', 'do', or 'don't' instructions.
    pattern = r"""
        mul\((\d{1,3}),(\d{1,3})\)
        |
        do\(\)
        |
        don't\(\)
    """
    for match in re.finditer(pattern, data, re.VERBOSE):
        instruction = match.group(0)
        if instruction == "don't()":
            mul_enabled = False
        elif instruction == "do()":
            mul_enabled = True
        # After we've found 'do()', we can get the instructions.
        elif mul_enabled:
            first, second = map(int, match.groups())
            res += first * second

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