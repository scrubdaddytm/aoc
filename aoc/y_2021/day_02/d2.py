from aoc.cli import file_input
from dataclasses import dataclass


def main() -> None:
    lines = []
    with file_input() as file:
        while line := file.readline():
            lines.append(line.split())

    horizontal = 0
    depth = 0

    aim = 0
    part_2_horizontal = 0
    part_2_depth = 0

    for line in lines:
        val = int(line[1])
        if line[0] == "up":
            depth -= val
            aim -= val
        elif line[0] == "down":
            depth += val
            aim += val
        else:
            horizontal += val
            part_2_horizontal += val
            part_2_depth += (aim * val)

    print(f"part 1: {horizontal * depth}")
    print(f"part 2: {part_2_horizontal * part_2_depth}")


if __name__ == "__main__":
    main()
