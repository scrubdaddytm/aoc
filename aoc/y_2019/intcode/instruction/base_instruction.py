class Instruction:
    parameter_count: int

    def run(
        self: "Instruction",
        memory: list[int],
        instruction_pointer: int,
    ) -> None:
        pass
