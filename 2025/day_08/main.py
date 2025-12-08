import fileinput  # noqa
import heapq  # noqa
import math  # noqa
import os  # noqa
import re  # noqa
import sys  # noqa
from collections import Counter, defaultdict, deque, namedtuple  # noqa
from functools import cache  # noqa
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


def part_one(input_file: str):
    def calc_euclidean_distance(
        box1: tuple[int, int, int], box2: tuple[int, int, int]
    ) -> float:
        x1, y1, z1 = box1
        x2, y2, z2 = box2
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

    def u_find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    def u_union(node1, node2):
        root1 = u_find(node1)
        root2 = u_find(node2)
        if root1 == root2:
            return False

        if rank[root1] > rank[root2]:
            parent[root2] = root1
            rank[root1] += rank[root2]
        else:
            parent[root1] = root2
            rank[root2] += rank[root1]

        return True

    data = parse_lines(input_file)
    coordinates = []
    for line in data:
        x, y, z = map(int, line.split(","))
        coordinates.append((x, y, z))
    length = len(data)

    # Create a list of edges sorted by Euclidean distance.
    edges: list[tuple[float, int, int]] = []
    for node1_index in range(length):
        for node2_index in range(node1_index + 1, length):
            if node1_index != node2_index:
                edges.append(
                    (
                        calc_euclidean_distance(
                            coordinates[node1_index], coordinates[node2_index]
                        ),
                        node1_index,
                        node2_index,
                    )
                )
    edges.sort()

    # Use union-find to group connected circuits (components) together.
    parent = [node_index for node_index in range(length)]
    rank = [1] * length
    for index in range(1000):
        _, node1, node2 = edges[index]
        u_union(node1, node2)

    # Find the largest circuit groups (components).
    circuits = set()
    for index in range(length):
        root = u_find(index)
        circuits.add((rank[root], root))
    sorted_circuits = sorted(list(circuits), reverse=True)

    # Return the sizes of the three largest circuits multiplied.
    return sorted_circuits[0][0] * sorted_circuits[1][0] * sorted_circuits[2][0]


def part_two(input_file: str):
    def calc_euclidean_distance(
        box1: tuple[int, int, int], box2: tuple[int, int, int]
    ) -> float:
        x1, y1, z1 = box1
        x2, y2, z2 = box2
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

    def u_find(node):
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    def u_union(node1, node2):
        root1 = u_find(node1)
        root2 = u_find(node2)
        if root1 == root2:
            return False

        if rank[root1] > rank[root2]:
            parent[root2] = root1
            rank[root1] += rank[root2]
        else:
            parent[root1] = root2
            rank[root2] += rank[root1]

        return True

    data = parse_lines(input_file)
    coordinates = []
    for line in data:
        x, y, z = map(int, line.split(","))
        coordinates.append((x, y, z))
    length = len(data)

    # Create a list of edges sorted by Euclidean distance.
    edges: list[tuple[float, int, int]] = []
    for node1_index in range(length):
        for node2_index in range(node1_index + 1, length):
            if node1_index != node2_index:
                edges.append(
                    (
                        calc_euclidean_distance(
                            coordinates[node1_index], coordinates[node2_index]
                        ),
                        node1_index,
                        node2_index,
                    )
                )
    edges.sort()

    parent = [node_index for node_index in range(length)]
    rank = [1] * length
    num_components = length

    # Use union-find to group connected circuits (components) together
    # until all components are connected.
    last_node1, last_node2 = -1, -1
    index = 0
    while num_components > 1:
        _, node1, node2 = edges[index]
        if u_union(node1, node2):
            num_components -= 1
            last_node1, last_node2 = node1, node2
        index += 1

    return coordinates[last_node1][0] * coordinates[last_node2][0]


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
