from aoc.y_2019.intcode.instruction.base_instruction import Instruction


class Product(Instruction):
    parameter_count: int = 3

    def run(
        self: "Instruction",
        memory: list[int],
        instruction_pointer: int,
    ) -> None:
        left_address = memory[instruction_pointer + 1]
        right_address = memory[instruction_pointer + 2]
        result_address = memory[instruction_pointer + 3]

        memory[result_address] = memory[left_address] * memory[right_address]
