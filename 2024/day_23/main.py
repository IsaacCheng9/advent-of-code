import heapq  # noqa
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


def part_one(input_file: str) -> int:
    lines = parse_lines(input_file)
    edges = [line.split("-") for line in lines]

    # Connections are bidirectional, so add each node to each other's set.
    edge_connections = defaultdict(set)
    for first, second in edges:
        edge_connections[first].add(second)
        edge_connections[second].add(first)

    # Find all sets of three nodes that are connected to each other.
    connected_triplets = set()
    for first in edge_connections:
        for second in edge_connections[first]:
            for third in edge_connections[second]:
                # Second is connected to first and third is connected to
                # second, so we just need to check if first is connected to
                # third for the triplet to be connected.
                if first != third and first in edge_connections[third]:
                    connected_triplets.add(tuple(sorted([first, second, third])))

    # Return the number of triplets where at least one computer starts with
    # the letter 't'.
    return len(
        [
            triplet
            for triplet in connected_triplets
            if any(computer.startswith("t") for computer in triplet)
        ]
    )


def part_two(input_file: str) -> str:
    def dfs_fully_connected_sets(node: str, cur_set: set[str]) -> None:
        """
        Performs a depth-first search to find all computers that are fully
        connected to each other.

        Args:
            node: The current computer we're exploring.
            cur_set: The set of computers that are fully connected to each
                     other.
        """
        # Convert the set to a sorted tuple to create a unique, hashable key.
        key = tuple(sorted(cur_set))
        # Skip if we've already explored this combination of computers to avoid
        # redundant exploration of sets reachable through different paths.
        if key in connected_sets:
            return
        # Add this set of fully connected computers to our collection.
        connected_sets.add(key)

        # Find all computers that could expand our fully connected set.
        for neighbour in edge_connections[node]:
            # Skip if the computer is already in our set or if it's not
            # directly connected to every computer in our current set.
            if neighbour in cur_set or not all(
                neighbour in edge_connections[query] for query in cur_set
            ):
                continue
            # Explore whether this neighbor can be part of a larger fully
            # connected set with our current computers.
            dfs_fully_connected_sets(neighbour, {*cur_set, neighbour})

    lines = parse_lines(input_file)
    edges = [line.split("-") for line in lines]

    # Connections are bidirectional, so add each node to each other's set.
    edge_connections = defaultdict(set)
    for first, second in edges:
        edge_connections[first].add(second)
        edge_connections[second].add(first)

    # Find all connected sets starting from each computer.
    connected_sets = set()
    for edge in edge_connections:
        dfs_fully_connected_sets(edge, {edge})

    # Return the largest connected set as a comma-separated string.
    largest_connected_set = sorted(max(connected_sets, key=len))
    return ",".join(largest_connected_set)


if __name__ == "__main__":
    day_path = Path(__file__).parent
    input_path = day_path / "input.txt"

    print("\n--- Part One ---")
    answer1, duration1 = execute_with_runtime(part_one, str(input_path))
    print(f"Answer: {answer1}")
    print(f"Runtime: {duration1:.4f} milliseconds")

    print("\n--- Part Two ---")
    answer2, duration2 = execute_with_runtime(part_two, str(input_path))
    print(f"Answer: {answer1}")
    print(f"Runtime: {duration2:.4f} milliseconds")

    print(f"\nTotal runtime: {duration1 + duration2:.4f} milliseconds")
