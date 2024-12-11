"""
Advent of Code solution template with enhanced utilities.
"""

from functools import cache
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
    # Use memoisation to avoid recomputing the same stone-step combinations.
    @cache
    def count_stones(stone, steps):
        # If no steps remain, we have one stone.
        if steps == 0:
            return 1
        # If the stone is 0, it's replaced by 1 in the next iteration.
        elif stone == 0:
            return count_stones(1, steps - 1)

        str_stone = str(stone)
        length = len(str_stone)
        mid = length // 2
        # If there are an even number of digits, split the stone in half and
        # count both halves.
        if length % 2 == 0:
            return count_stones(int(str_stone[:mid]), steps - 1) + count_stones(
                int(str_stone[mid:]), steps - 1
            )
        # Otherwise, multiply the stone by 2024 and continue counting.
        return count_stones(stone * 2024, steps - 1)

    input_data = parse_input(file_name)
    stones = [int(stone) for stone in input_data.split()]
    # Sum the count for each stone after 25Z steps.
    return sum(count_stones(stone, 25) for stone in stones)


def part_two(file_name: str) -> int:
    # Use memoisation to avoid recomputing the same stone-step combinations.
    @cache
    def count_stones(stone, num_steps):
        # If no steps remain, we have one stone.
        if num_steps == 0:
            return 1
        # If the stone is 0, it's replaced by 1 in the next iteration.
        elif stone == 0:
            return count_stones(1, num_steps - 1)

        str_stone = str(stone)
        length = len(str_stone)
        mid = length // 2
        # If there are an even number of digits, split the stone in half and
        # count both halves.
        if length % 2 == 0:
            return count_stones(int(str_stone[:mid]), num_steps - 1) + count_stones(
                int(str_stone[mid:]), num_steps - 1
            )
        # Otherwise, multiply the stone by 2024 and continue counting.
        return count_stones(stone * 2024, num_steps - 1)

    input_data = parse_input(file_name)
    stones = [int(stone) for stone in input_data.split()]
    # Sum the count for each stone after 75 steps.
    return sum(count_stones(stone, 75) for stone in stones)


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
