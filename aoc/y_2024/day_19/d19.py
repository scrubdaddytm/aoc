from functools import cache

from aoc.cli import file_input


@cache
def find_combo(towels: tuple[str], target: str) -> int:
    if not target:
        return 1

    possibilities = 0
    for towel in towels:
        if towel == target[: len(towel)]:
            possibilities += find_combo(towels, target[len(towel):])

    return possibilities


def main() -> None:
    towels = None
    p1 = p2 = 0
    with file_input() as file:
        while line := file.readline().strip():
            towels = tuple(line.split(", "))
        while line := file.readline().strip():
            possibilities = find_combo(towels, line)
            p1 += 1 if possibilities else 0
            p2 += possibilities
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
