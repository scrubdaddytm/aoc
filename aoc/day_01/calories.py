import numpy as np
import heapq

from aoc.cli import file_input


def max_calores(puzzle_input: dict[int, list[int]]) -> (int, int):
    top_elves = []
    for elf_num, items in puzzle_input.items():
        cals = np.sum(items)
        heapq.heappush(top_elves, (cals, elf_num))
        if len(top_elves) > 3:
            heapq.heappop(top_elves)
    print(f"{top_elves=}")
    return np.sum(np.fromiter((elf[0] for elf in top_elves), int))


def main() -> None:
    with file_input() as file:
        puzzle_input = {}
        elf_num = 0
        while line := file.readline():
            if line != "\n":
                items = puzzle_input.setdefault(elf_num, [])
                items.append(int(line))
            else:
                elf_num += 1

    result = max_calores(puzzle_input)
    print(f"{result=}")


if __name__ == "__main__":
    main()
