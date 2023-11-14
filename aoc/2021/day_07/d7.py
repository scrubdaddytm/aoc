from aoc.cli import file_input
from dataclasses import dataclass
from statistics import median


def main() -> None:
    positions = []
    with file_input() as file:
        while line := file.readline().strip():
            positions = list(map(int, line.split(",")))
    print(f"{positions}")

    med = int(median(positions))
    fuel = 0
    for position in positions:
        fuel += abs(position - med)

    print(f"part 1: moved to {med} and cost {fuel}")


if __name__ == "__main__":
    main()
