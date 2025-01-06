from aoc.cli import file_input
from aoc.geometry import Point
from itertools import combinations
from bisect import bisect


def expand(
    galaxies: list[Point],
    dup_rows: list[int],
    dup_cols: list[int],
    expand_value: int = 1,
) -> int:
    expanded = []
    for galaxy in galaxies:
        row_count = bisect(dup_rows, galaxy.y)
        col_count = bisect(dup_cols, galaxy.x)
        row_mult = len(dup_rows[:row_count])
        col_mult = len(dup_cols[:col_count])
        expanded.append(
            galaxy.move(Point(col_mult * expand_value, row_mult * expand_value))
        )
        print(
            f"{galaxy} + ({col_mult*expand_value}, {row_mult*expand_value}) -> {expanded[-1]}"
        )
    return expanded


def main() -> None:
    lines = []
    with file_input() as file:
        while line := file.readline().strip():
            lines.append(list(line))

    dup_rows = []
    for idx, line in enumerate(lines):
        if all(char == "." for char in line):
            dup_rows.append(idx)

    dup_cols = []
    for idx in range(len(lines[0])):
        if all(line[idx] == "." for line in lines):
            dup_cols.append(idx)

    galaxies = []
    for y, row in enumerate(lines):
        for x, col in enumerate(row):
            if col == "#":
                galaxies.append(Point(x, y))

    expanded_galaxies = expand(galaxies, dup_rows, dup_cols)

    shortest_path_sum = 0
    for a, b in combinations(expanded_galaxies, 2):
        shortest_path_sum += a.distance(b)

    print(f"Part 1: {shortest_path_sum}")

    expanded_galaxies_p2 = expand(galaxies, dup_rows, dup_cols, 999_999)
    shortest_path_sum = 0
    for a, b in combinations(expanded_galaxies_p2, 2):
        shortest_path_sum += a.distance(b)

    print(f"Part 2: {shortest_path_sum}")


if __name__ == "__main__":
    main()
