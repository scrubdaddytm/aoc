from typing import Self
from aoc.cli import file_input
from dataclasses import dataclass
from aoc.geometry import Point
from aoc.geometry import right
from aoc.geometry import left
from aoc.geometry import down
from copy import deepcopy
import uuid
import pathlib


@dataclass
class Rock:
    points: list[Point]

    def max_height(self):
        return max([p.y for p in self.points])

    def raise_to_height(self, height: int) -> Self:
        self.points = [Point(p.x, p.y + height + 1) for p in self.points]
        return self

    def adjust(self, direction: callable, rock_points: set[Point]) -> bool:
        if self.can_move(direction, rock_points):
            self.points = [direction(point) for point in self.points]
            return True
        return False

    def can_move(self, direction: callable, rock_points: set[Point]) -> bool:
        result = set([direction(point) for point in self.points])
        xs = set([p.x for p in result])
        ys = set([p.y for p in result])
        return all([
            not result & rock_points,
            max(xs) < 7,
            min(xs) >= 0,
            min(ys) >= 0,
        ])

"""
####

.#.
###
.#.

..#
..#
#
#
#
#

##
##
"""

SHAPES = [
    Rock(points=[Point(2, 3), Point(3, 3), Point(4, 3), Point(5, 3)]), # LINE
    Rock(points=[Point(2, 4), Point(3, 4), Point(3, 5), Point(3, 3), Point(4, 4)]), # CROSS
    Rock(points=[Point(2, 3), Point(3, 3), Point(4, 3), Point(4, 4), Point(4, 5)]), # BACKWARDS L
    Rock(points=[Point(2, 3), Point(2, 4), Point(2, 5), Point(2, 6)]), # lowercase l
    Rock(points=[Point(2, 3), Point(2, 4), Point(3, 4), Point(3, 3)]), # square
]
DIRECTION = {
    "<": left,
    ">": right,
}

def get_next_shape(stopped_shapes: int, height: int) -> Rock:
    return deepcopy(SHAPES[stopped_shapes % len(SHAPES)]).raise_to_height(height)

def print_rocks(points: set[Point], height: int, falling: Rock = None, to_std_out: bool = False) -> None:
    display = [["." for _ in range(7)] for _ in range(height + 7)]

    for point in points:
        display[-(point.y+1)][point.x] = "#"
    if falling:
        for point in falling.points:
            display[-(point.y+1)][point.x] = "@"

    if to_std_out:
        for row in display:
            print(f"|{''.join(row)}|")
        print(f"+-------+")
        print()
    else:
        path = pathlib.Path(f"d17_run_{uuid.uuid4()}.tmp")
        with path.open('w') as display_out:
            for row in display:
                display_out.write(f"|{''.join(row)}|\n")
            display_out.write(f"+-------+\n")
        print(path)


def simulate(jet_pattern: list[chr], stopped_rocks_target: int = 2022) -> int:
    # width = 7
    stopped_rocks = 0
    rock_points = set()
    height = -1
    jet = 0
    jet_len = len(jet_pattern)

    while stopped_rocks < stopped_rocks_target:
        shape = get_next_shape(stopped_rocks, height)
        dropping = True
        while dropping:
            shape.adjust(DIRECTION[jet_pattern[jet]], rock_points)
            jet = (jet + 1) % jet_len
            dropping = shape.adjust(down, rock_points)
        stopped_rocks += 1
        rock_points |= set(shape.points)
        height = max(height, shape.max_height())
        if stopped_rocks % 1_000_000 == 0:
            print(f"Rock {stopped_rocks}")

    if stopped_rocks_target < 10_000:
        print_rocks(rock_points, height)
    return height + 1


def main() -> None:
    lines = []
    with file_input() as file:
        while line := file.readline():
            lines.append(line)
    height = simulate(lines[0])
    print(f"{height}")

    # height = simulate(lines[0], 1_000_000_000_000)
    # print(f"{height}")


if __name__ == "__main__":
    main()