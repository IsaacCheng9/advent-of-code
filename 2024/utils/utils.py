from typing import Any, Callable
import time


def execute_with_runtime(func: Callable, *args, **kwargs) -> tuple[Any, float]:
    """
    Executes a function and returns its result along with runtime (ms).
    """
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()
    runtime = (end - start) * 1000
    return result, runtime


def parse_input(file_path: str) -> str:
    """
    Reads and returns the input data with leading and trailing whitespace
    removed.
    """
    with open(file_path) as f:
        return f.read().strip()


def parse_lines(file_path: str) -> list[str]:
    """Reads and returns the input split into lines."""
    return parse_input(file_path).split("\n")


def parse_list_of_ints(file_path: str) -> list[int]:
    """Reads and returns the input as a list of integers."""
    return [int(x) for x in parse_lines(file_path)]


def parse_2d_grid_strs(file_path: str) -> list[list[str]]:
    """Reads and returns the input as a 2D grid of strings."""
    return [list(line) for line in parse_lines(file_path)]


def parse_2d_grid_ints(file_path: str) -> list[list[int]]:
    """Reads and returns the input as a 2D grid of integers."""
    return [[int(char) for char in line] for line in parse_lines(file_path)]


def calculate_manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    """Calculate the Manhattan distance between two points."""
    return abs(x1 - x2) + abs(y1 - y2)
