from aoc.cli import file_input
from dataclasses import dataclass


def main() -> None:
    lines = []
    with file_input() as file:
        while line := file.readline():
            lines.append(int(line))
    increases = 0
    prev_depth = lines[0]
    for depth in lines[1:]:
        if depth > prev_depth:
            increases += 1
        prev_depth = depth
    print(f"part 1: {increases}")

    increases_pt2 = 0
    prev_window = lines[0] + lines[1] + lines[2]
    for i, depth in enumerate(lines[3:], start=3):
        new_window = prev_window + depth - lines[i-3]
        if new_window > prev_window:
            increases_pt2 += 1
        prev_window = new_window

    print(f"part 2: {increases_pt2}")


if __name__ == "__main__":
    main()
