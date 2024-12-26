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
import heapq

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
    grid = parse_2d_grid_strs(file_name)
    ROWS = len(grid)
    COLS = len(grid[0])

    # Find the starting position.
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == "S":
                start_row = row
                start_col = col
                break
        else:
            continue
        break

    queue = [(0, start_row, start_col, 0, 1)]
    # Track seen states to avoid unnecessary recomputation.
    # State is represented as (row, col, row_diff, col_diff), where row_diff
    # and col_diff represent the direction of movement:
    # (0, -1) is up, (0, 1) is down, (-1, 0) is left, (1, 0) is right.
    # We start facing right.
    seen = {(start_row, start_col, 0, 1)}

    # Perform BFS to find the shortest path to the end tile.
    while queue:
        cost, row, col, row_diff, col_diff = heapq.heappop(queue)
        seen.add((row, col, row_diff, col_diff))
        # If we've found the end tile, exit the BFS.
        if grid[row][col] == "E":
            break

        # Evaluate the next possible moves.
        for new_cost, new_row, new_col, new_row_diff, new_col_diff in [
            # Forward movement costs 1.
            (cost + 1, row + row_diff, col + col_diff, row_diff, col_diff),
            # 90-degree clockwise rotation costs 1000.
            (cost + 1000, row, col, col_diff, -row_diff),
            # 90-degree counter-clockwise rotation costs 1000.
            (cost + 1000, row, col, -col_diff, row_diff),
        ]:
            # Only add valid moves to the queue.
            if (
                grid[new_row][new_col] == "#"
                or (new_row, new_col, new_row_diff, new_col_diff) in seen
            ):
                continue
            heapq.heappush(
                queue, (new_cost, new_row, new_col, new_row_diff, new_col_diff)
            )

    return cost


def part_two(file_name: str) -> int:
    grid = parse_2d_grid_strs(file_name)
    ROWS = len(grid)
    COLS = len(grid[0])

    # Find the starting position.
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == "S":
                start_row = row
                start_col = col
                break
        else:
            continue
        break

    # Track the states for BFS in a priority queue.
    # [ (total_score, cur_row, cur_col, cur_row_diff, cur_col_diff) ]
    # State is represented as (row, col, row_diff, col_diff), where row_diff
    # and col_diff represent the direction of movement:
    # (0, -1) is up, (0, 1) is down, (-1, 0) is left, (1, 0) is right.
    # We start facing right.
    queue = [(0, start_row, start_col, 0, 1)]
    # Track the lowest cost to reach a state (position and direction).
    lowest_cost_per_state = {(start_row, start_col, 0, 1): 0}
    # Store all previously states that led to each state.
    backtrack = {}
    # Track the lowest cost found and all end states with that cost.
    lowest_cost = float("inf")
    end_states = set()

    # Perform BFS to find all optimal paths.
    while queue:
        cost, row, col, row_diff, col_diff = heapq.heappop(queue)
        # Skip if we've already found a better way to get to this state.
        if cost > lowest_cost_per_state.get(
            (row, col, row_diff, col_diff), float("inf")
        ):
            continue
        # If we've found the end tile, check whether the cost is better or
        # equal to the lowest cost found so far. If so, add it to the end
        # states.
        if grid[row][col] == "E":
            if cost > lowest_cost:
                break
            lowest_cost = cost
            end_states.add((row, col, row_diff, col_diff))

        # Evaluate the next possible moves.
        for new_cost, new_row, new_col, new_row_diff, new_col_diff in [
            # Forward movement costs 1.
            (cost + 1, row + row_diff, col + col_diff, row_diff, col_diff),
            # 90-degree clockwise rotation costs 1000.
            (cost + 1000, row, col, col_diff, -row_diff),
            # 90-degree counter-clockwise rotation costs 1000.
            (cost + 1000, row, col, -col_diff, row_diff),
        ]:
            # Skip if we're moving into a wall.
            if grid[new_row][new_col] == "#":
                continue

            # Get the lowest known cost to reach the new state.
            lowest = lowest_cost_per_state.get(
                (new_row, new_col, new_row_diff, new_col_diff), float("inf")
            )
            # Skip if we've already found a better way to get to this state.
            if new_cost > lowest:
                continue

            # If we've found a new best path to this state, reset the backtrack
            # paths and update the lowest cost for this state.
            if new_cost < lowest:
                backtrack[(new_row, new_col, new_row_diff, new_col_diff)] = set()
                lowest_cost_per_state[
                    (new_row, new_col, new_row_diff, new_col_diff)
                ] = new_cost

            # Add the current state to the backtrack path for the new state.
            backtrack[(new_row, new_col, new_row_diff, new_col_diff)].add(
                (row, col, row_diff, col_diff)
            )
            # Add the new state to the queue for further exploration.
            heapq.heappush(
                queue, (new_cost, new_row, new_col, new_row_diff, new_col_diff)
            )

    # Reconstruct all tiles that are part of any optimal path. Start with all
    # end states and work backwards.
    states = deque(end_states)
    seen = set(end_states)

    # Use BFS to find all states that can lead to an optimal end state.
    while states:
        key = states.popleft()
        for last in backtrack.get(key, []):
            if last in seen:
                continue
            seen.add(last)
            states.append(last)

    # Return the number of unique tiles (ignoring direction) that are part of
    # any optimal path.
    return len({(row, col) for row, col, _, _ in seen})


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
