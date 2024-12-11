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
    execute_with_runtime,
    parse_input_without_trailing_and_leading_whitespace,
    parse_lines,
    parse_ints,
    parse_2d_grid,
    calculate_manhattan_distance,
)


def part_one(file_name: str) -> int:
    input_data = open(file_name).read().strip()
    disk = []
    file_id = 0

    # Parse input string where even indices are file lengths and odd indices
    # are space lengths (e.g. : '2333' means 2 blocks of file ID 0, 3 spaces,
    # 3 blocks of file ID 1, 3 spaces).
    for index, char in enumerate(input_data):
        length = int(char)
        # At even indices, add the file IDs to the disk.
        if index % 2 == 0:
            disk += [file_id] * length
            file_id += 1
        # At odd indices, add empty spaces represented by -1s to the disk.
        else:
            disk += [-1] * length

    # Get positions of all empty spaces (-1s) in the disk
    blanks = [index for index, char in enumerate(disk) if char == -1]

    # Process each empty space from left to right, and move the rightmost file
    # block into the current empty space.
    for blank in blanks:
        # Remove trailing empty spaces so we can get the rightmost file block.
        while disk[-1] == -1:
            disk.pop()
        # Stop if there are no more file blocks to move.
        if blank > len(disk):
            break
        # Move the rightmost file block into the current empty space.
        disk[blank] = disk.pop()

    # Calculate checksum by multiplying each position by its file ID.
    return sum(index * char for index, char in enumerate(disk))


def part_two(file_name: str) -> int:
    input_data = open(file_name).read().strip()
    # Track file positions and lengths for each file ID.
    # {file_id: (position, length)}
    files = {}
    # Store the position and length of each empty space: [(position, length)]
    # This enables us ot efficiently find spaces where files can be moved.
    blanks = []
    file_id = 0
    file_start_pos = 0

    # Parse input string where even indices are file lengths and odd indices
    # are space lengths (e.g. : '2333' means 2 blocks of file ID 0, 3 spaces,
    # 3 blocks of file ID 1, 3 spaces).
    for index, char in enumerate(input_data):
        length = int(char)
        # At even indices, store the file position and length.
        if index % 2 == 0:
            files[file_id] = (file_start_pos, length)
            file_id += 1
        # At odd indices, store any non-zero length empty spaces.
        else:
            # Avoid storing empty spaces of length 0 as this will slow down the
            # process of moving files.
            if length != 0:
                blanks.append((file_start_pos, length))
        file_start_pos += length

    # Process files in reverse order (highest ID to lowest) to move each file
    # to the leftmost possible position where it fits completely.
    while file_id > 0:
        # We added an extra file ID at the end of the loop, so decrement it at
        # the start instead of the end of the loop.
        file_id -= 1
        file_pos, file_size = files[file_id]

        # Check each empty space from left to right to find where the file
        # can be moved.
        for blank_index, (blank_start, blank_length) in enumerate(blanks):
            # Stop checking spaces that start after the file's current position
            # since we only want to move files left.
            if blank_start >= file_pos:
                blanks = blanks[:blank_index]
                break

            # If the file fits in this empty space, move it there and update
            # the remaining empty space.
            if file_size <= blank_length:
                files[file_id] = (blank_start, file_size)
                # If the file exactly fills the space, remove the empty space.
                if file_size == blank_length:
                    blanks.pop(blank_index)
                # If the file partially fills the space, update the remaining
                # empty space size.
                else:
                    blanks[blank_index] = (
                        blank_start + file_size,
                        blank_length - file_size,
                    )
                # We want to move each file exactly once, so break if it fits.
                break

    # Calculate checksum by multiplying each position by its file ID.
    checksum = 0
    for file_id, (file_start_pos, file_length) in files.items():
        file_positions = range(file_start_pos, file_start_pos + file_length)
        for pos in file_positions:
            checksum += file_id * pos

    return checksum


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
