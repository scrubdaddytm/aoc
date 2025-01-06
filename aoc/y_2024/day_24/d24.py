import re
from collections import defaultdict, deque
from copy import copy

from aoc.cli import file_input


def perform_op(left_operand: int, operator: str, right_operand: int) -> int:
    match operator:
        case "AND":
            return left_operand & right_operand
        case "OR":
            return left_operand | right_operand
        case "XOR":
            return left_operand ^ right_operand


def simulate(
    gates: dict[str, int],
    operations: list[tuple[str, str, str, str]],
) -> int | None:
    gate_copy = copy(gates)
    q = deque(operations)

    unsuccesful = 0
    while q:
        if len(q) == unsuccesful:
            return None
        operation = q.popleft()
        left_operand, operator, right_operand, result_gate = operation

        if left_operand in gate_copy and right_operand in gate_copy:
            gate_copy[result_gate] = perform_op(
                gate_copy[left_operand],
                operator,
                gate_copy[right_operand],
            )
            unsuccesful = 0
        else:
            q.append(operation)
            unsuccesful += 1

    return gates_to_int(gate_copy, "z")


def gates_to_int(gates: dict[str, int], prefix: str) -> int:
    gate_pairs = filter(lambda pair: pair[0][0] == prefix, gates.items())
    result = 0
    for k, v in sorted(gate_pairs, reverse=True):
        result <<= 1
        result |= v
    return result


def try_adding(
    gates: dict[str, int],
    operations: dict[dict[dict[str, str]]],
) -> list[tuple[str, str]]:
    carry = None
    for i in range(44):
        x = f"x{i:02}"
        y = f"y{i:02}"
        z = None

        xy_xor_result = operations[x][y]["XOR"]
        print(f"    x ^ y = {xy_xor_result}")
        xy_and_result = operations[x][y]["AND"]
        print(f"    x & y = {xy_and_result}")

        carry_and_result = None
        if carry:
            # Full Adder
            z = operations[xy_xor_result][carry]["XOR"]
            carry_and_result = operations[xy_xor_result][carry]["AND"]
            print(f"    (x ^ y) & c = {carry_and_result}")
            carry = operations[xy_and_result][carry_and_result]["OR"]
        else:
            # Half Adder
            z = xy_xor_result
            carry = xy_and_result

        print(f"{x} + {y} = {z} with {carry}")

        if z != f"z{i:02}":
            raise ValueError(z)


def main() -> None:
    gates = {}
    operations = []
    ops_by_gate = defaultdict(lambda: defaultdict(dict))
    with file_input() as file:
        while line := file.readline().strip():
            gate, val = line.split(": ")
            gates[gate] = int(val)
        while line := file.readline().strip():
            matches = re.findall(r"(...) (AND|OR|XOR) (...) -> (...)", line)
            operations.append(matches[0])
            l, op, r, res = matches[0]
            ops_by_gate[l][r][op] = res
            ops_by_gate[r][l][op] = res

    x_val = gates_to_int(gates, "x")
    y_val = gates_to_int(gates, "y")
    expected = x_val + y_val

    print(f"x: {x_val}")
    print(f"y: {y_val}")
    p1 = simulate(gates, operations)

    print(f"EXP: {expected:b}\nACT: {p1:b}")

    try_adding(gates, ops_by_gate)

    """
    Shameless manual evaluation of the errors that were raised from `try_adding`.

    Example logs:
    [...]
        x36 + y36 = z36 with nwb
        x ^ y = vcr
        x & y = dgn
        (x ^ y) & c = z37
    [...]
      File "/Users/tucker/pg/aoc/aoc/2024/day_24/d24.py", line 105, in try_adding
        carry = operations[xy_and_result][carry_and_result]["OR"]
                ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
    KeyError: 'z37'

    🫠
    """
    swaps = [("z05", "gdd"), ("z09", "cwt"), ("jmv", "css"), ("z37", "pqt")]

    flat_swaps = [a for swap in swaps for a in swap]
    p2 = ",".join(sorted(flat_swaps))

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
