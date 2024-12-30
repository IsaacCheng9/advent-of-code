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
    def calculate_next_secret_number(num):
        # Step 1: multiply by 64 and perform bitwise XOR modulo 16777216
        num = (num ^ (num * 64)) % MODULO_VAL
        # Step 2: divide by 32 and perform bitwise XOR modulo 16777216
        num = (num ^ (num // 32)) % MODULO_VAL
        # Step 3: multiply by 2048 and perform bitwise XOR modulo 16777216
        num = (num ^ (num * 2048)) % MODULO_VAL

        return num

    initial_secret_nums = parse_lines(input_file)
    MODULO_VAL = 16777216
    sum_of_secret_num_2000 = 0

    # For each initial secret number, calculate the 2000th secret number by
    # applying the three steps 2000 times.
    for secret_num in initial_secret_nums:
        num = int(secret_num)
        for _ in range(2000):
            num = calculate_next_secret_number(num)
        # Add the 2000th secret number to the sum.
        sum_of_secret_num_2000 += num

    return sum_of_secret_num_2000


def part_two(input_file: str) -> int:
    def calculate_next_secret_number(num):
        # Step 1: multiply by 64 and perform bitwise XOR modulo 16777216
        num = (num ^ (num * 64)) % MODULO_VAL
        # Step 2: divide by 32 and perform bitwise XOR modulo 16777216
        num = (num ^ (num // 32)) % MODULO_VAL
        # Step 3: multiply by 2048 and perform bitwise XOR modulo 16777216
        num = (num ^ (num * 2048)) % MODULO_VAL

        return num

    initial_secret_nums = parse_lines(input_file)
    MODULO_VAL = 16777216
    # Store the total value for each difference sequence between 5 prices.
    # { (diff1, diff2, diff3, diff4): total_val_sold }
    diff_sequences_to_total: dict[tuple[int, int, int, int], int] = defaultdict(int)

    for secret_num in initial_secret_nums:
        num = int(secret_num)

        # Store the last digit of each secret number in the buyer price list.
        buyer_prices = [num % 10]
        for _ in range(2000):
            num = calculate_next_secret_number(num)
            buyer_prices.append(num % 10)

        seen_sequences: set[tuple[int, int, int, int]] = set()
        # For each sliding window of 5 prices, get the consecutive differences
        # and add the fifth price to the total for that sequence if the
        # differences sequence hasn't been seen before.
        for i in range(len(buyer_prices) - 4):
            first, second, third, fourth, fifth = buyer_prices[i : i + 5]
            diff_sequence = (
                second - first,
                third - second,
                fourth - third,
                fifth - fourth,
            )

            # If the sequence has been seen before, skip to the next sequence.
            if diff_sequence in seen_sequences:
                continue
            # Otherwise, add the fifth price to the total for that sequence,
            # and increment the sequence total to represent a sell.
            seen_sequences.add(diff_sequence)
            diff_sequences_to_total[diff_sequence] += fifth

    # Return the maximum total value from any sequence.
    return max(diff_sequences_to_total.values())


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
