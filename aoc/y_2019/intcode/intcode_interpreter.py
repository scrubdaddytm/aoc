from copy import copy

from aoc.y_2019.intcode import OPCODE_TO_INSTRUCTION, Opcode


class Intcode:

    memory: list[int] | None = None

    def __init__(self: "Intcode", memory: list[int]) -> None:
        self.memory = copy(memory)

    def set_memory(self: "Intcode", memory: list[int]) -> None:
        self.memory = copy(memory)

    def run(self: "Intcode") -> None:
        if not self.memory:
            raise ValueError("You must provide a memory input.")

        instruction_pointer = 0
        while (op := self.memory[instruction_pointer]) != Opcode.TERMINATE:
            instruction = OPCODE_TO_INSTRUCTION[op]
            instruction.run(self.memory, instruction_pointer)
            instruction_pointer += instruction.parameter_count + 1
