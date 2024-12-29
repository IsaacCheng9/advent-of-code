"""
Advent of Code solution template with enhanced utilities.
"""

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
    def find_button_sequences(keypad: list[str]) -> dict[tuple, list[str]]:
        """
        Finds all possible shortest paths between any two buttons on a keypad
        using BFS. For each pair of buttons, it computes the optimal sequence
        of directional moves needed to move from one button to the other.

        Args:
            keypad: A 2D list representing the layout of the keypad.

        Returns:
            A dictionary mapping each pair of buttons to a list of optimal
            sequences of directional moves needed to move from one button to
            the other. All sequences will have the same length.
        """
        rows = len(keypad)
        cols = len(keypad[0])

        # Create a mapping of each button to its (row, col) position on the
        # keypad.
        button_positions = {}
        for row in range(len(keypad)):
            for col in range(len(keypad[row])):
                if keypad[row][col] is not None:
                    button_positions[keypad[row][col]] = (row, col)

        # For each pair of buttons, find all optimal paths between them.
        paths = {}
        for start_button in button_positions:
            for end_button in button_positions:
                # If start and end buttons are the same, just press 'A' to
                # activate the button.
                if start_button == end_button:
                    paths[(start_button, end_button)] = ["A"]
                    continue

                valid_paths = []
                # Initialise BFS with the starting position and the empty path.
                queue = deque([(button_positions[start_button], "")])
                shortest_path = float("inf")

                # Perform BFS to find all valid paths between the start and end
                # buttons.
                while queue:
                    (row, col), cur_path = queue.popleft()
                    # Try moving in all four directions.
                    for new_row, new_col, direction in [
                        (row - 1, col, "^"),
                        (row + 1, col, "v"),
                        (row, col - 1, "<"),
                        (row, col + 1, ">"),
                    ]:
                        # Skip moves that would go off the keypad or hit empty
                        # spaces.
                        if (
                            new_row not in range(rows)
                            or new_col not in range(cols)
                            or keypad[new_row][new_col] is None
                        ):
                            continue

                        # Check if we've reached the end button.
                        if keypad[new_row][new_col] == end_button:
                            # If we've found a longer path, stop exploring this
                            # branch as continuing would only yield longer
                            # paths.
                            if shortest_path < len(cur_path) + 1:
                                break
                            # Otherwise, add it to the list of valid paths.
                            shortest_path = len(cur_path) + 1
                            valid_paths.append(cur_path + direction + "A")
                        # Continue exploring the path until we reach the end.
                        else:
                            queue.append(((new_row, new_col), cur_path + direction))
                    # Use a for-else loop to break out of the while loop if
                    # we've found a valid path.
                    else:
                        # Only reached if the for loop completes normally.
                        continue
                    break  # Only reached if the for loop is broken.

                # Store the valid paths for the current button pair.
                paths[(start_button, end_button)] = valid_paths

        return paths

    def find_possible_sequences(code: str) -> list[str]:
        """
        Generates all possible sequences of moves that could type a given code.
        Each sequence represents one way to move between the buttons needed to
        type the code.

        Args:
            code: The code to type.

        Returns:
            A list of all possible sequences of moves that could type the code.
        """
        # Get a list of possible sequences for each button transition.
        # e.g. going from A to 1 on the keypad could be one of:
        # ['^<<A', '<^<A'], so this list would be the first element in the
        # output list for code 169A.
        sequence_options = [numeric_sequences[(x, y)] for x, y in zip("A" + code, code)]
        # Join all permutations of these sequences to get all possible ways to
        # type the code in a 1D array.
        return ["".join(sequence) for sequence in product(*sequence_options)]

    @cache
    def get_path_length(sequence: str, depth: int = 2) -> int:
        """
        Recursively calculates the minimum number of button presses needed to
        generate a sequence at a given depth in the robot chain.

        Args:
            sequence: The sequence to generate.
            depth: Current depth in the robot chain. At depth 2, we calculate
                   how many button presses the first robot must make to control
                   the second robot. e.g. for '029A' it calculates each
                   transition in the sequence A -> 0, 0 -> 2, 2-> 9, 9 -> A. At
                   depth 1, we're at the final robot that's typing on the
                   numerical keypad. Defaults at 2 because we have the final
                   robot, and the robot controlling that final robot.

        Returns:
            The minimum number of button presses needed to generate the
            sequence.
        """
        # Base case: at depth 1, just sum up the lengths of the directional
        # sequences, as the final robot is typing on the numerical keypad.
        if depth == 1:
            return sum(
                directional_sequence_lengths[(x, y)]
                for x, y in zip("A" + sequence, sequence)
            )

        # Otherwise, we need to calculate the minimum number of button presses
        # needed for the robot controlling the next robot in the chain using
        # the directional keypad.
        # For each button transition, find the minimum length needed to
        # generate it.
        total_length = 0
        for x, y in zip("A" + sequence, sequence):
            total_length += min(
                get_path_length(subseq, depth - 1)
                for subseq in directional_sequences[(x, y)]
            )
        return total_length

    lines = parse_lines(input_file)
    # Define the layout of both keypads
    NUMERIC_KEYPAD = [
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        [None, "0", "A"],
    ]
    DIRECTIONAL_KEYPAD = [
        [None, "^", "A"],
        ["<", "v", ">"],
    ]

    # Calculate all possible sequences between buttons for both keypads.
    numeric_sequences = find_button_sequences(NUMERIC_KEYPAD)
    directional_sequences = find_button_sequences(DIRECTIONAL_KEYPAD)
    # Store the length of each directional sequence for quick lookup.
    directional_sequence_lengths = {
        key: len(value[0]) for key, value in directional_sequences.items()
    }

    # Calculate total complexity by processing each code.
    total_complexity = 0
    for code in lines:
        # Find all ways to type this code on the numeric keypad.
        possible_sequences = find_possible_sequences(code)
        # Calculate the minimum length needed to generate any of these
        # sequences.
        min_length = min(map(get_path_length, possible_sequences))
        # Add this code's complexity (length * numeric value) to the total.
        total_complexity += min_length * int(code[:-1])

    return total_complexity


# !IMPORTANT: Same as part_one, but with default depth set to 25.
def part_two(input_file: str) -> int:
    def find_button_sequences(keypad: list[str]) -> dict[tuple, list[str]]:
        """
        Finds all possible shortest paths between any two buttons on a keypad
        using BFS. For each pair of buttons, it computes the optimal sequence
        of directional moves needed to move from one button to the other.

        Args:
            keypad: A 2D list representing the layout of the keypad.

        Returns:
            A dictionary mapping each pair of buttons to a list of optimal
            sequences of directional moves needed to move from one button to
            the other. All sequences will have the same length.
        """
        rows = len(keypad)
        cols = len(keypad[0])

        # Create a mapping of each button to its (row, col) position on the
        # keypad.
        button_positions = {}
        for row in range(len(keypad)):
            for col in range(len(keypad[row])):
                if keypad[row][col] is not None:
                    button_positions[keypad[row][col]] = (row, col)

        # For each pair of buttons, find all optimal paths between them.
        paths = {}
        for start_button in button_positions:
            for end_button in button_positions:
                # If start and end buttons are the same, just press 'A' to
                # activate the button.
                if start_button == end_button:
                    paths[(start_button, end_button)] = ["A"]
                    continue

                valid_paths = []
                # Initialise BFS with the starting position and the empty path.
                queue = deque([(button_positions[start_button], "")])
                shortest_path = float("inf")

                # Perform BFS to find all valid paths between the start and end
                # buttons.
                while queue:
                    (row, col), cur_path = queue.popleft()
                    # Try moving in all four directions.
                    for new_row, new_col, direction in [
                        (row - 1, col, "^"),
                        (row + 1, col, "v"),
                        (row, col - 1, "<"),
                        (row, col + 1, ">"),
                    ]:
                        # Skip moves that would go off the keypad or hit empty
                        # spaces.
                        if (
                            new_row not in range(rows)
                            or new_col not in range(cols)
                            or keypad[new_row][new_col] is None
                        ):
                            continue

                        # Check if we've reached the end button.
                        if keypad[new_row][new_col] == end_button:
                            # If we've found a longer path, stop exploring this
                            # branch as continuing would only yield longer
                            # paths.
                            if shortest_path < len(cur_path) + 1:
                                break
                            # Otherwise, add it to the list of valid paths.
                            shortest_path = len(cur_path) + 1
                            valid_paths.append(cur_path + direction + "A")
                        # Continue exploring the path until we reach the end.
                        else:
                            queue.append(((new_row, new_col), cur_path + direction))
                    # Use a for-else loop to break out of the while loop if
                    # we've found a valid path.
                    else:
                        # Only reached if the for loop completes normally.
                        continue
                    break  # Only reached if the for loop is broken.

                # Store the valid paths for the current button pair.
                paths[(start_button, end_button)] = valid_paths

        return paths

    def find_possible_sequences(code: str) -> list[str]:
        """
        Generates all possible sequences of moves that could type a given code.
        Each sequence represents one way to move between the buttons needed to
        type the code.

        Args:
            code: The code to type.

        Returns:
            A list of all possible sequences of moves that could type the code.
        """
        # Get a list of possible sequences for each button transition.
        # e.g. going from A to 1 on the keypad could be one of:
        # ['^<<A', '<^<A'], so this list would be the first element in the
        # output list for code 169A.
        sequence_options = [numeric_sequences[(x, y)] for x, y in zip("A" + code, code)]
        # Join all permutations of these sequences to get all possible ways to
        # type the code in a 1D array.
        return ["".join(sequence) for sequence in product(*sequence_options)]

    @cache
    def get_path_length(sequence: str, depth: int = 25) -> int:
        """
        Recursively calculates the minimum number of button presses needed to
        generate a sequence at a given depth in the robot chain.

        Args:
            sequence: The sequence to generate.
            depth: Current depth in the robot chain. At depth 2, we calculate
                   how many button presses the first robot must make to control
                   the second robot. e.g. for '029A' it calculates each
                   transition in the sequence A -> 0, 0 -> 2, 2-> 9, 9 -> A. At
                   depth 1, we're at the final robot that's typing on the
                   numerical keypad. Defaults at 25 because we have a chain of
                   robots controlling each other until we reach the final
                   robot that uses the numerical keypad.

        Returns:
            The minimum number of button presses needed to generate the
            sequence.
        """
        # Base case: at depth 1, just sum up the lengths of the directional
        # sequences.
        if depth == 1:
            return sum(
                directional_sequence_lengths[(x, y)]
                for x, y in zip("A" + sequence, sequence)
            )

        # Otherwise, we need to calculate the minimum number of button presses
        # needed for the robot controlling the next robot in the chain using
        # the directional keypad.
        # For each button transition, find the minimum length needed to
        # generate it.
        total_length = 0
        for x, y in zip("A" + sequence, sequence):
            total_length += min(
                get_path_length(subseq, depth - 1)
                for subseq in directional_sequences[(x, y)]
            )
        return total_length

    lines = parse_lines(input_file)
    # Define the layout of both keypads
    NUMERIC_KEYPAD = [
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        [None, "0", "A"],
    ]
    DIRECTIONAL_KEYPAD = [
        [None, "^", "A"],
        ["<", "v", ">"],
    ]

    # Calculate all possible sequences between buttons for both keypads.
    numeric_sequences = find_button_sequences(NUMERIC_KEYPAD)
    directional_sequences = find_button_sequences(DIRECTIONAL_KEYPAD)
    # Store the length of each directional sequence for quick lookup.
    directional_sequence_lengths = {
        key: len(value[0]) for key, value in directional_sequences.items()
    }

    # Calculate total complexity by processing each code.
    total_complexity = 0
    for code in lines:
        # Find all ways to type this code on the numeric keypad.
        possible_sequences = find_possible_sequences(code)
        # Calculate the minimum length needed to generate any of these
        # sequences.
        min_length = min(map(get_path_length, possible_sequences))
        # Add this code's complexity (length * numeric value) to the total.
        total_complexity += min_length * int(code[:-1])

    return total_complexity


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
