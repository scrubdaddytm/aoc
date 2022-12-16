from aoc.cli import file_input
from dataclasses import dataclass


def main() -> None:
    lines = []
    with file_input() as file:
        while line := file.readline():
            lines.append(line)
    print(f"{lines}")


if __name__ == "__main__":
    main()