import re

from aoc.cli import file_input
from aoc.print_tools import Color

"""
combo ops:
    0 - 3 == 0 - 3
    4 == A
    5 == B
    6 == C
    7 == failmode

0 - adv : A = A / 2^ combo op
1 - bxl : B = B ^ literal op
2 - bst : B = combo op % 8
3 - jnz : if A != 0, set instruction to value of literal operand. No +2 on op after.
4 - bxc : B = B ^ C (reads op, doesnt use)
5 - out : print combo % 8 with a comma
6 - bdv : B = A / 2^ combo op
7 - cdv : C = A / 2^ combo op
"""

INSTS = {
    0: "adv",
    1: "bxl",
    2: "bst",
    3: "jnz",
    4: "bxc",
    5: Color.GREEN + "out" + Color.END,
    6: "bdv",
    7: "cdv",
}
DEBUG = False


def p(out: str) -> None:
    if DEBUG:
        print(out, end=" -- ")


def get_combo_op(op: int, registers: list[int]):
    if op <= 3:
        return op
    elif op <= 6:
        return registers[op - 4]
    raise ValueError("NO SEVENS FOR THE LOVE OF GOD")


def simulate(registers: list[int], program: list[int]) -> list[int]:
    instruction = 0
    output = []
    while instruction < len(program) - 1:
        op = program[instruction + 1]
        p(
            f"-- {INSTS[program[instruction]]} {program[instruction+1]}->{op=}: {registers}"
        )
        inc = 2
        match program[instruction]:
            case 0:
                op = get_combo_op(op, registers)
                p(f"A = {registers[0]} >> {op}")
                registers[0] = registers[0] >> op
            case 1:
                p(f"B = {registers[1]} ^ {op}")
                registers[1] = registers[1] ^ op
            case 2:
                op = get_combo_op(op, registers)
                p(f"B = {op} % 8")
                registers[1] = op % 8
            case 3:
                if registers[0] != 0:
                    instruction = op
                    inc = 0
            case 4:
                p(f"B = {registers[1]} ^ {registers[2]}")
                registers[1] = registers[1] ^ registers[2]
            case 5:
                op = get_combo_op(op, registers)
                output.append(op % 8)
            case 6:
                op = get_combo_op(op, registers)
                p(f"B = {registers[0]} >> {op}")
                registers[1] = registers[0] >> op
            case 7:
                op = get_combo_op(op, registers)
                p(f"C = {registers[0]} >> {op}")
                registers[2] = registers[0] >> op
        instruction += inc
        p("\n")
    return output


def list_to_int(a_list: list[int]) -> int:
    a = 0
    for a_oct in a_list:
        a <<= 3
        a |= a_oct
    return a


def backtrack(
    program: list[int],
    a_trips: list[int],
    p_idx: int,
) -> int | None:
    if p_idx < 0:
        a = list_to_int(a_trips)
        result = simulate([a, 0, 0], program)
        if result == program:
            print(f" {result=}")
            return a
        return None

    for potential_a_oct in range(8):
        maybe_a = a_trips + [potential_a_oct]
        a = list_to_int(maybe_a)

        simulated_result = simulate([a, 0, 0], program)

        if simulated_result == program[p_idx:]:
            result = backtrack(program, maybe_a, p_idx - 1)
            if result:
                return result

    return None


def main() -> None:
    registers = []
    program = []
    with file_input() as file:
        while line := file.readline().strip():
            registers.extend(map(int, re.findall(r"(\d+)", line)))
        program = list(map(int, re.findall(r"(\d)", file.readline().strip())))

    p1 = simulate(registers, program)

    p2 = backtrack(program, [], len(program) - 1)
    print(f"{program=}")

    print(f"Part 1: {','.join(map(str, p1))}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
