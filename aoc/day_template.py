from aoc.cli import file_input
from dataclasses import dataclass


def main() -> None:
    lines = []
    with file_input() as file:
        while line := file.readline():
            lines.append(line)
    print(f"{lines}")

    p1 = 0
    p2 = 0

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
