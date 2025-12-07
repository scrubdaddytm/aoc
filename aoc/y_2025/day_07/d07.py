from collections import defaultdict

from aoc.cli import file_input


def main() -> None:
    lines = []
    with file_input() as file:
        while line := file.readline().strip():
            lines.append(line)

    p1 = 0
    p2 = 0

    s = 0
    while lines[0][s] != "S":
        s += 1

    lasers = {s: 1}
    for line in lines[1:]:
        new_lasers = defaultdict(int)
        for laser, count in lasers.items():
            if line[laser] == "^":
                new_lasers[laser - 1] += count
                new_lasers[laser + 1] += count
                p1 += 1
            else:
                new_lasers[laser] += count
        lasers = new_lasers

    p2 = sum([c for c in lasers.values()])

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
