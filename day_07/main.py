"""
Advent of Code solution template with enhanced utilities.
"""

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
    run_with_timing,
    parse_input_without_trailing_and_leading_whitespace,
    parse_lines,
    parse_ints,
    parse_2d_grid,
    calculate_manhattan_distance,
)


def part_one(file_name: str) -> int:
    def can_obtain(target: int, array: list[int]) -> bool:
        # Base case: if only one number remains, we can't apply further
        # operations, so check if it equals the target.
        if len(array) == 1:
            return target == array[0]

        # Apply the operation on the last number and check the remaining
        # array. We use the last number even though operations are done from
        # left-to-right because  we're backtracking from the target to the
        # first number.
        last_num = array[-1]
        remaining_array = array[:-1]
        # Try both multiplication and addition with the last number.
        if (
            # Multiplication: if the target is divisible by the last number,
            # check if we can get target / number with the new array.
            (target % last_num == 0 and can_obtain(target // last_num, remaining_array))
            # Addition: if the target is greater than the last number, check if
            # we can get target - number with the new array.
            or (target > last_num and can_obtain(target - last_num, remaining_array))
        ):
            return True

        return False

    input = open(file_name)
    total_calibration_result = 0

    for line in input:
        # The left number is the target, and the right numbers are the array.
        left, right = line.split(": ")
        target = int(left)
        array = [int(x) for x in right.split()]
        # If we can obtain the target by applying operations on the numbers in
        # the array from left to right, increment by the target.
        if can_obtain(target, array):
            total_calibration_result += int(target)

    return total_calibration_result


def part_two(file_name: str) -> int:
    def can_obtain(target: int, array: list[int]) -> bool:
        # Base case: if only one number remains, we can't apply further
        # operations, so check if it equals the target.
        if len(array) == 1:
            return target == array[0]

        # Apply the operation on the last number and check the remaining
        # array. We use the last number even though operations are done from
        # left-to-right because  we're backtracking from the target to the
        # first number.
        last_num = array[-1]
        remaining_array = array[:-1]
        # Convert the last number and target to strings for the concatenation
        # check.
        str_last = str(last_num)
        str_target = str(target)
        # Try multiplication, addition, and concatenation with the last number.
        if (
            # Multiplication: if the target is divisible by the last number,
            # check if we can get target / number with the new array.
            (target % last_num == 0 and can_obtain(target // last_num, remaining_array))
            # Addition: if the target is greater than the last number, check if
            # we can get target - number with the new array.
            or (target > last_num and can_obtain(target - last_num, remaining_array))
            # Concatenation: if target ends with the last number as a string,
            # check if we can get the remaining prefix with the new array.
            or (
                len(str_target) > len(str_last)
                and str_target.endswith(str_last)
                # Check if the remaining prefix can be obtained with the new
                # target with the end (str_last) removed.
                and can_obtain(int(str_target[: -len(str_last)]), remaining_array)
            )
        ):
            return True

        return False

    input = open(file_name)
    total_calibration_result = 0

    for line in input:
        # The left number is the target, and the right numbers are the array.
        left, right = line.split(": ")
        target = int(left)
        array = [int(x) for x in right.split()]
        # If we can obtain the target by applying operations on the numbers in
        # the array from left to right, increment by the target.
        if can_obtain(target, array):
            total_calibration_result += target

    return total_calibration_result


if __name__ == "__main__":
    day_path = Path(__file__).parent
    input_path = day_path / "input.txt"

    print("\n--- Part One ---")
    answer1, duration1 = run_with_timing(part_one, str(input_path))
    print(f"Answer: {answer1}")
    print(f"Time: {duration1:.4f} seconds")

    print("\n--- Part Two ---")
    answer2, duration2 = run_with_timing(part_two, str(input_path))
    print(f"Answer: {answer2}")
    print(f"Time: {duration2:.4f} seconds")

    print(f"\nTotal time: {duration1 + duration2:.4f} seconds")
