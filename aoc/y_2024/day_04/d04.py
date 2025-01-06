from aoc.cli import file_input
from dataclasses import dataclass
from aoc.geometry import DIRECTIONS
from aoc.geometry import up, right, down, left
from aoc.geometry import CARDINAL_DIRECTIONS
from aoc.geometry import Point
from aoc.geometry import in_bounds
from aoc.print_tools import print_grid


xmas = ("X", "M", "A", "S")


def check_cell(grid, i, j):
    if grid[i][j] != "X":
        return 0

    words = 0
    for direction in DIRECTIONS:
        m = direction(Point(i, j))
        a = direction(m)
        s = direction(a)
        if (
            in_bounds(s, len(grid), len(grid[0]))
            and grid[m.x][m.y] == "M"
            and grid[a.x][a.y] == "A"
            and grid[s.x][s.y] == "S"
        ):
            words += 1
    return words


def check_cell_x(grid, i, j, seen):
    if grid[i][j] != "M":
        return 0

    words = 0

    m_1 = Point(i, j)
    for a_dir, b_dir in (
        (up, right),
        (up, left),
        (right, up),
        (right, down),
        (down, right),
        (down, left),
        (left, down),
        (left, up),
    ):
        m_2 = a_dir(a_dir(m_1))
        a = a_dir(b_dir(m_1))
        s_1 = b_dir(b_dir(m_1))
        s_2 = b_dir(b_dir(m_2))
        if (
            in_bounds(s_2, len(grid), len(grid[0]))
            and grid[m_2.x][m_2.y] == "M"
            and grid[a.x][a.y] == "A"
            and grid[s_1.x][s_1.y] == "S"
            and grid[s_2.x][s_2.y] == "S"
        ):
            # print_grid(
            #     {m_1: "M", m_2: "M", a: "A", s_1: "S", s_2: "S"},
            #     max_x=len(grid),
            #     max_y=len(grid[0]),
            #     min_x=0,
            #     min_y=0,
            # )
            mmass = frozenset([m_1, m_2, a, s_1, s_2])
            if mmass not in seen:
                words += 1
                seen.add(mmass)
    return words


def main() -> None:
    grid = []
    with file_input() as file:
        while line := file.readline().strip():
            grid.append(line)

    p1 = 0
    p2 = 0

    seen = set()
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            p1 += check_cell(grid, i, j)
            p2 += check_cell_x(grid, i, j, seen)

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
