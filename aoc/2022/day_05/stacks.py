import re
from copy import deepcopy
from dataclasses import dataclass

from aoc.cli import file_input


@dataclass
class Procedure:
    count: int
    start: int
    target: int


def parse_procedure(raw_input: str) -> Procedure:
    match = re.match(r"move (?P<count>\d+) from (?P<start>\d+) to (?P<target>\d+)", raw_input)
    return Procedure(int(match["count"]), int(match["start"]), int(match["target"]))


def rearrange_9001(initial_position: list[list[str]], rearrangement_procedures: list[Procedure]) -> None:
    stacks = deepcopy(initial_position)
    for procedure in rearrangement_procedures:
        start_stack = stacks[procedure.start-1]
        stacks[procedure.target-1] += start_stack[len(start_stack)-procedure.count:]
        del start_stack[len(start_stack)-procedure.count:]
    return stacks


def rearrange_9000(initial_position: list[list[str]], rearrangement_procedures: list[Procedure]) -> list[list[str]]:
    stacks = deepcopy(initial_position)
    for procedure in rearrangement_procedures:
        for idx in range(procedure.count):
            stacks[procedure.target-1].append(stacks[procedure.start-1].pop())
    return stacks


def parse_initial_position(initial_position_raw: list[str]) -> list[list[str]]:
    stack_count = len(initial_position_raw.pop().strip().split())
    stacks = [ [] for i in range(stack_count) ]

    for stack_layer in reversed(initial_position_raw):
        for idx in range(0, len(stack_layer)-1, 4):
            value = stack_layer[idx+1]
            if value != " ":
                stacks[idx // 4].append(value)

    return stacks


def main() -> None:
    initial_position_input = []
    rearrangement_procedures = []

    with file_input() as file:
        while (line := file.readline()) != "\n":
            initial_position_input.append(line)

        while line := file.readline().strip():
            rearrangement_procedures.append(parse_procedure(line))

    stacks = parse_initial_position(initial_position_input)

    r1_result = rearrange_9000(stacks, rearrangement_procedures)
    print(f"9000: {''.join([stack[-1] if len(stack) else '~' for stack in r1_result])}")

    r2_result = rearrange_9001(stacks, rearrangement_procedures)
    print(f"9001: {''.join([stack[-1] if len(stack) else '~' for stack in r2_result])}")


if __name__ == "__main__":
    main()
