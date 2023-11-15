from aoc.cli import file_input
from dataclasses import dataclass


SEGMENT_COUNTS = {
    2: 1,
    4: 4,
    3: 7,
    7: 8,
}


def main() -> None:
    lines = []
    with file_input() as file:
        while line := file.readline().strip():
            split_line = line.split(" | ")
            lines.append((split_line[0].split(), split_line[1].split()))

    easy_numbers = 0
    for (patterns, outputs) in lines:
        for output in outputs:
            if len(output) in SEGMENT_COUNTS:
                easy_numbers += 1

    print(f"part 1: {easy_numbers=}")


if __name__ == "__main__":
    main()
