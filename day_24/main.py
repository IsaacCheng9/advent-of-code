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
    def calculate_wire_value(wire: str) -> int:
        """
        Recursively calculates the value of a wire by evaluating its gate
        connections and input values. Uses memoization to store computed wire
        values, ensuring each wire is only calculated once even if it's used as
        input to multiple gates.

        Args:
            wire: The wire to calculate the value for.

        Returns:
            The integer value of the wire after applying the boolean operator.
        """
        if wire in initial_wires_map:
            return initial_wires_map[wire]

        operator, first_wire, second_wire = gate_connections_map[wire]
        # Compute and memoise the result by recursively calculating input wires
        # and applying the boolean operator.
        initial_wires_map[wire] = BOOLEAN_OPERATORS[operator](
            calculate_wire_value(first_wire), calculate_wire_value(second_wire)
        )

        return initial_wires_map[wire]

    input_data = parse_input(input_file)
    # Split input into two sections: initial wire values and gate connections.
    initial_wires, gate_connections = input_data.split("\n\n")
    # Map the boolean operators to their bitwise operations in Python.
    BOOLEAN_OPERATORS = {
        "OR": lambda x, y: x | y,
        "AND": lambda x, y: x & y,
        "XOR": lambda x, y: x ^ y,
    }

    # Create a map of wires from the initial values.
    initial_wires_map = {}
    for line in initial_wires.splitlines():
        first_wire, second_wire = line.split(": ")
        initial_wires_map[first_wire] = int(second_wire)
    # Create a map of gates and their connections, where each gate is
    # represented by its output wire and stores its operation type and input
    # wires. This allows us to recursively evaluate the circuit starting from
    # any wire.
    # { output_wire: (boolean_gate, first_wire, second_wire) }
    gate_connections_map: dict[str, tuple[str, str, str]] = {}
    for line in gate_connections.splitlines():
        # Remove the arrow so we can split the line into parts by spaces.
        first_wire, boolean_gate, second_wire, output_wires = line.replace(
            " -> ", " "
        ).split()
        gate_connections_map[output_wires] = (boolean_gate, first_wire, second_wire)

    # Process all output wires (z00 to zNN) in sequential order.
    output_wires = []
    wire_index = 0
    while True:
        wire_name = f"z{wire_index:02d}"
        # If the wire is not in the gate connections map, we have reached the
        # end of the circuit.
        if wire_name not in gate_connections_map:
            break
        output_wires.append(calculate_wire_value(wire_name))
        wire_index += 1

    # Convert the sequence of binary digits to decimal. We reverse the list
    # because z00 represents the least significant bit, z01 the next bit, and
    # so on, forming a binary number from right to left.
    return int("".join(map(str, output_wires[::-1])), base=2)


# !IMPORTANT: Took a long time to work out the logic for this part.
def part_two(input_file: str) -> str:
    def count_valid_positions() -> int:
        """
        Counts how many bit positions follow the correct addition pattern.

        Returns:
            The number of bit positions that follow the correct addition
            pattern.
        """
        position = 0
        while True:
            if not verify_wire_pattern(f"z{position:02d}", position):
                break
            position += 1
        return position

    def verify_wire_pattern(cur_wire: str, bit_position: int) -> bool:
        """
        Recursively verifies if a wire's gate connections match the expected
        pattern for binary addition at the given bit position.

        Args:
            cur_wire: The current wire to verify.
            bit_position: The bit position to verify.

        Returns:
            Whether the wire's gate connections match the expected pattern.
        """
        if cur_wire not in gate_connections_map:
            return False

        operator, first_wire, second_wire = gate_connections_map[cur_wire]
        # For binary addition, the output bit must be the XOR of the inputs
        # and any carry from the previous bit.
        if operator != "XOR":
            return False

        # Base case: the first bit (z00) should be a direct XOR of x00 and y00,
        # as there's no previous position to generate a carry.
        if bit_position == 0:
            return sorted([first_wire, second_wire]) == ["x00", "y00"]

        # For higher positions, each output bit is the XOR of:
        # 1. The intermediate XOR of the input bits at this position
        # 2. The carry computation from previous positions, which may have
        #    propagated through multiple positions.
        return (
            check_intermediate_xor(first_wire, bit_position)
            and check_carry_computation(second_wire, bit_position)
        ) or (
            check_intermediate_xor(second_wire, bit_position)
            and check_carry_computation(first_wire, bit_position)
        )

    def check_intermediate_xor(cur_wire: str, bit_position: int) -> bool:
        """
        Checks if this gate computes the XOR of the input bits at this
        position, which is one component of the binary addition.

        Args:
            cur_wire: The wire to check.
            bit_position: The bit position to check.

        Returns:
            Whether the wire represents the XOR of two input bits.
        """
        if cur_wire not in gate_connections_map:
            return False

        operator, first_wire, second_wire = gate_connections_map[cur_wire]
        # The intermediate result must be computed using XOR.
        if operator != "XOR":
            return False

        # Check if the gate XORs the correct input bits for this position.
        expected_wires = [f"x{bit_position:02d}", f"y{bit_position:02d}"]
        return sorted([first_wire, second_wire]) == expected_wires

    def check_carry_computation(cur_wire: str, bit_position: int) -> bool:
        """
        Checks if a wire represents the carry bit computation for binary
        addition. For position 1, this is a simple AND of x00 and y00. For
        higher positions, it combines direct carry generation (using AND) with
        carry propagation (using OR).

        Args:
            cur_wire: The wire to check.
            bit_position: The bit position to check.

        Returns:
            Whether the wire represents the carry bit computation.
        """
        if cur_wire not in gate_connections_map:
            return False

        operator, first_wire, second_wire = gate_connections_map[cur_wire]
        # For position 1, we only need to check for a carry from the first
        # position (x00 AND y00), since there are no previous positions to
        # generate carries.
        if bit_position == 1:
            if operator != "AND":
                return False
            return sorted([first_wire, second_wire]) == ["x00", "y00"]

        # For higher positions, we need to combine two types of carries with
        # OR:
        # 1. A direct carry generated at the previous position
        # 2. A propagated carry that may have come through from even earlier
        #    positions
        if operator != "OR":
            return False

        # Check the carry computation using the previous position's bits.
        prev_pos = bit_position - 1
        return (
            check_direct_carry(first_wire, prev_pos)
            and check_propagated_carry(second_wire, prev_pos)
        ) or (
            check_direct_carry(second_wire, prev_pos)
            and check_propagated_carry(first_wire, prev_pos)
        )

    def check_direct_carry(wire: str, bit_position: int) -> bool:
        """
        Checks if a wire computes the direct carry from two input bits, which
        is when both input bits are 1.

        Args:
            wire: The wire to check.
            bit_position: The bit position to check.

        Returns:
            Whether the wire computes the direct carry from two input bits.
        """
        if wire not in gate_connections_map:
            return False

        operator, first_wire, second_wire = gate_connections_map[wire]
        # Direct carry is computed using AND of input bits.
        if operator != "AND":
            return False

        # Check if this gate generates a carry by ANDing the input bits at this
        # position.
        expected_wires = [f"x{bit_position:02d}", f"y{bit_position:02d}"]
        return sorted([first_wire, second_wire]) == expected_wires

    def check_propagated_carry(wire: str, bit_position: int) -> bool:
        """
        Checks if a wire computes the propagated carry through XOR gates,
        which is when a carry moves through multiple positions.

        Args:
            wire: The wire to check.
            bit_position: The bit position to check.

        Returns:
            Whether the wire computes the propagated carry through XOR gates.
        """
        if wire not in gate_connections_map:
            return False

        operator, first_wire, second_wire = gate_connections_map[wire]
        # Propagated carry requires AND of intermediate XOR and previous carry.
        if operator != "AND":
            return False

        # When a carry propagates through a position, we need:
        # 1. The current position's bits to be different (checked by
        #    intermediate XOR)
        # 2. A carry coming in from any previous position
        # This allows carries to "ripple" through multiple positions when
        # needed.
        return (
            check_intermediate_xor(first_wire, bit_position)
            and check_carry_computation(second_wire, bit_position)
        ) or (
            check_intermediate_xor(second_wire, bit_position)
            and check_carry_computation(first_wire, bit_position)
        )

    # Parse input and initialize gate connections map
    input_data = parse_input(input_file)
    # Split input into two sections: initial wire values and gate connections.
    _, gate_connections = input_data.split("\n\n")

    # Create a map of gates and their connections, where each gate is
    # represented by its output wire and stores its operation type and input
    # wires. This allows us to recursively evaluate the circuit starting from
    # any wire.
    # { output_wire: (boolean_gate, first_wire, second_wire) }
    gate_connections_map: dict[str, tuple[str, str, str]] = {}
    for line in gate_connections.splitlines():
        # Remove the arrow so we can split the line into parts by spaces.
        first_wire, boolean_gate, second_wire, output_wire = line.replace(
            " -> ", " "
        ).split()
        gate_connections_map[output_wire] = (boolean_gate, first_wire, second_wire)

    # Iteratively find the four pairs of swapped gates by trying all
    # combinations.
    swapped_wires = []
    for _ in range(4):
        num_valid_positions_before_swap = count_valid_positions()
        found_swap = False
        for gate1 in gate_connections_map:
            # If we've found a swap in a previous iteration of gate1, skip it
            # as we can only swap the same wire once.
            if found_swap:
                break

            for gate2 in gate_connections_map:
                if gate1 == gate2:
                    continue
                # Try swapping gates and check if it improves the correctness
                # of the circuit.
                gate_connections_map[gate1], gate_connections_map[gate2] = (
                    gate_connections_map[gate2],
                    gate_connections_map[gate1],
                )
                # If the swap improved the circuit, track this swap and break
                # so we can move onto the next gate1.
                if count_valid_positions() > num_valid_positions_before_swap:
                    swapped_wires.extend([gate1, gate2])
                    found_swap = True
                    break
                # Restore the original configuration if the swap didn't improve
                # the circuit.
                gate_connections_map[gate1], gate_connections_map[gate2] = (
                    gate_connections_map[gate2],
                    gate_connections_map[gate1],
                )

    return ",".join(sorted(swapped_wires))


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
