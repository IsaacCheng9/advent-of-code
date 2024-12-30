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
import functools

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
    def is_ordered(update):
        # For every pair in the update list, check if the ordering rule is
        # valid. Return False if any rule is invalid.
        for before_index in range(len(update)):
            for after_index in range(before_index + 1, len(update)):
                before = update[before_index]
                after = update[after_index]
                # If 'before' has 'after' in its set of numbers that must come
                # before it, this means we've found a violation - 'after'
                # appears after 'before' when it should appear before it.
                if after in nums_before_mapping[before]:
                    return False
        return True

    data = open(file_name)
    # The first block contains the page ordering rules, and the second block
    # contains the page update numbers.
    page_ordering_rules, page_update_nums = data.read().split("\n\n")
    # Split the rules and updates into lists so we can iterate over them.
    page_ordering_rules = page_ordering_rules.strip().split("\n")
    page_update_nums = page_update_nums.strip().split("\n")
    total_sum = 0

    # Create a cache to map each number to the set of numbers that must come
    # before it.
    # e.g. {3: {1, 2}} means that 3 must come after 1 and 2.
    nums_before_mapping = defaultdict(set)
    for line in page_ordering_rules:
        before, after = map(int, line.split("|"))
        nums_before_mapping[after].add(before)

    for line in page_update_nums:
        # Convert the comma-separated string to a list of integers.
        update = list(map(int, line.split(",")))
        # If the update is ordered, add the middle number to the total sum.
        if is_ordered(update):
            total_sum += update[len(update) // 2]

    return total_sum


def part_two(file_name: str) -> int:
    def is_ordered(update):
        # For every pair in the update list, check if the ordering rule is
        # valid. Return False if any rule is invalid.
        for before_index in range(len(update)):
            for after_index in range(before_index + 1, len(update)):
                before = update[before_index]
                after = update[after_index]
                # If 'before' has 'after' in its set of numbers that must come
                # before it, this means we've found a violation - 'after'
                # appears after 'before' when it should appear before it.
                if after in nums_before_mapping[before]:
                    return False
        return True

    def compare_pages(x, y):
        # Determine the relative ordering of two pages based on the rules.
        # -1 if x comes before y, 1 if y comes before x, 0 if they are equal.
        if x in nums_before_mapping[y]:
            return -1
        if y in nums_before_mapping[x]:
            return 1
        return 0

    data = open(file_name)
    # The first block contains the page ordering rules, and the second block
    # contains the page update numbers.
    page_ordering_rules, page_update_nums = data.read().split("\n\n")
    # Split the rules and updates into lists so we can iterate over them.
    page_ordering_rules = page_ordering_rules.strip().split("\n")
    page_update_nums = page_update_nums.strip().split("\n")
    total_sum = 0

    # Create a cache to map each number to the set of numbers that must come
    # before it.
    # e.g. {3: {1, 2}} means that 3 must come after 1 and 2.
    nums_before_mapping = defaultdict(set)
    for line in page_ordering_rules:
        before, after = map(int, line.split("|"))
        nums_before_mapping[after].add(before)

    for line in page_update_nums:
        # Convert the comma-separated string to a list of integers.
        update = list(map(int, line.split(",")))
        # If the update is not ordered, sort it and add the middle number.
        if not is_ordered(update):
            # Use a custom comparison function to sort the pages based on the
            # ordering rules, then add the middle number in the sorted list to
            # the total sum.
            update.sort(key=functools.cmp_to_key(compare_pages))
            total_sum += update[len(update) // 2]

    return total_sum


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
