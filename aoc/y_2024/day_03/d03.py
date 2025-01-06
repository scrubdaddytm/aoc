from aoc.cli import file_input
from dataclasses import dataclass
import re
from math import prod


def main() -> None:
    lines = []
    with file_input() as file:
        while line := file.readline().strip():
            lines.append(line)

    p1 = 0
    p2 = 0

    pattern = re.compile(r"mul\(\d+,\d+\)|do\(\)|don\'t\(\)")
    mul = True
    for line in lines:
        matches = pattern.findall(line)
        for match in matches:
            if match[0:3] == "mul":
                nums = list(map(int, match[4:-1].split(",")))
                product = prod(nums)
                p1 += product
                if mul:
                    p2 += product
            elif match[0:3] == "don":
                mul = False
            else:
                mul = True

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
