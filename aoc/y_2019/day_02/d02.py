from aoc.cli import file_input
from aoc.y_2019.intcode.intcode_interpreter import Intcode


def find_noun_and_verb(
    initial_memory: list[int],
    noun_idx: int = 1,
    verb_idx: int = 2,
) -> int:
    for noun in range(100):
        for verb in range(100):
            intcode_interpreter = Intcode(initial_memory)
            intcode_interpreter.memory[noun_idx] = noun
            intcode_interpreter.memory[verb_idx] = verb
            intcode_interpreter.run()
            if intcode_interpreter.memory[0] == 19690720:
                return (100 * noun) + verb
    raise ValueError("unable to find satisfactory noun and verb")


def main() -> None:
    p1 = p2 = 0
    initial_memory = []
    with file_input() as file:
        while line := file.readline().strip():
            initial_memory.extend(list(map(int, line.split(","))))

    intcode_interpreter = Intcode(initial_memory)

    NOUN_IDX = 1
    VERB_IDX = 2

    intcode_interpreter.memory[NOUN_IDX] = 12
    intcode_interpreter.memory[VERB_IDX] = 2

    intcode_interpreter.run()

    p1 = intcode_interpreter.memory[0]
    print(f"Part 1: {p1}")

    p2 = find_noun_and_verb(initial_memory)
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
