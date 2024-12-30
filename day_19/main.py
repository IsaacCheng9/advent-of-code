import heapq  # NOQA
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
from functools import cache

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


def part_one(input_file: str) -> int:
    lines = parse_lines(input_file)
    # Convert patterns to a hash set for O(1) lookups.
    patterns = set(lines[0].split(", "))
    # Find the longest pattern to limit the recursion path.
    max_pattern_length = max(map(len, patterns))
    # The second block of our input contains the desired designs.
    desired_designs = lines[2:]

    @cache
    def can_create_design(design: str) -> bool:
        # Base case: empty string means we've successfully matched the entire
        # design.
        if design == "":
            return True

        # Try all possible patterns up to the shortest of the remaining design
        # length and the longest available pattern.
        for i in range(min(len(design), max_pattern_length) + 1):
            # If we find a valid pattern and can create the remaining design,
            # we can create the entire design.
            if design[:i] in patterns and can_create_design(design[i:]):
                return True

        return False

    # Count how many designs we can create.
    return sum(1 if can_create_design(design) else 0 for design in desired_designs)


def part_two(input_file: str) -> int:
    lines = parse_lines(input_file)
    # Convert patterns to a hash set for O(1) lookups.
    patterns = set(lines[0].split(", "))
    # Find the longest pattern to limit the recursion path.
    max_pattern_length = max(map(len, patterns))
    # The second block of our input contains the desired designs.
    desired_designs = lines[2:]

    @cache
    def count_num_possible_designs(design: str) -> int:
        # Base case: empty string means we've successfully matched the entire
        # design.
        if design == "":
            return 1

        # Count how many designs we can create from this point onwards.
        num_possible_designs = 0
        # Try all possible patterns up to the shortest of the remaining design
        # length and the longest available pattern.
        for i in range(min(len(design), max_pattern_length) + 1):
            # If we find a valid pattern, add the number of ways to create the
            # remaining design to our total count.
            if design[:i] in patterns:
                num_possible_designs += count_num_possible_designs(design[i:])

        return num_possible_designs

    # Sum the number of possible combinations for each desired design.
    return sum(count_num_possible_designs(design) for design in desired_designs)


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
