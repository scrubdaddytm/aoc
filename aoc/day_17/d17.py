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
    name: str

    def max_height(self):
        return max([p.y for p in self.points])

    def raise_to_height(self, height: int) -> Self:
        self.points = [Point(p.x, p.y + height + 1) for p in self.points]
        return self

    def adjust(self, direction: callable, rock_points: dict[dict[int, bool]]) -> bool:
        new_points = []
        for p in self.points:
            d = direction(p)
            if rock_points.get(d.y, {}).get(d.x) or d.y < 0 or d.x < 0 or d.x >= 7:
                return False
            new_points.append(d)
        self.points = new_points
        return True

SHAPES = [
    Rock(points=[Point(2, 3), Point(3, 3), Point(4, 3), Point(5, 3)], name="LINE"), # LINE
    Rock(points=[Point(2, 4), Point(3, 4), Point(3, 5), Point(3, 3), Point(4, 4)], name="CROSS"), # CROSS
    Rock(points=[Point(2, 3), Point(3, 3), Point(4, 3), Point(4, 4), Point(4, 5)], name="BACK_L"), # BACKWARDS L
    Rock(points=[Point(2, 3), Point(2, 4), Point(2, 5), Point(2, 6)], name="LOWER_L"), # lowercase l
    Rock(points=[Point(2, 3), Point(2, 4), Point(3, 4), Point(3, 3)], name="SQUARE"), # square
]
DIRECTION = {
    "<": left,
    ">": right,
}

def get_next_shape(stopped_shapes: int, height: int) -> Rock:
    return deepcopy(SHAPES[stopped_shapes % len(SHAPES)]).raise_to_height(height)

def print_rocks(points: dict[dict[int, bool]], height: int, falling: Rock = None, to_std_out: bool = False) -> None:
    if to_std_out:
        for y in range(height+7):
            row = ["#" if points.get(height+7-y, {}).get(x, False) else "." for x in range(7)]
            if falling:
                for p in falling.points:
                    if p.y == y:
                        row[p.x] = "@"
            print(f"|{''.join(row)}|")
        print(f"+-------+")
        print()
    else:
        path = pathlib.Path(f"d17_run_{uuid.uuid4()}.tmp")
        with path.open('w') as display_out:
            for y in range(height+7):
                row = ["#" if points.get(height+7-y, {}).get(x, False) else "." for x in range(7)]
                if falling:
                    for p in falling.points:
                        if p.y == y:
                            row[p.x] = "@"
                display_out.write(f"|{''.join(row)}|\n")
            display_out.write(f"+-------+\n")
        print(path)


def simulate(jet_pattern: list[chr], stopped_rocks_target: int = 2022) -> int:
    stopped_rocks = 0
    rock_points_dict = {}
    height = -1
    jet = 0
    jet_len = len(jet_pattern)
    prev_movements = []
    heights = [0]
    while stopped_rocks < stopped_rocks_target:
        shape = get_next_shape(stopped_rocks, height)
        dropping = True
        shape_start = shape.points[0]
        shape_diff = Point(0, 0)
        while dropping:
            shape.adjust(DIRECTION[jet_pattern[jet]], rock_points_dict)
            jet = (jet + 1) % jet_len
            dropping = shape.adjust(down, rock_points_dict)

        shape_diff = Point(shape_start.x - shape.points[0].x, shape_start.y - shape.points[0].y)
        prev_movements.append((shape_diff, shape.name))

        stopped_rocks += 1

        for point in shape.points:
            y = rock_points_dict.setdefault(point.y, {})
            y[point.x] = True
            if len(y.keys()) == 7:
                for key in list(rock_points_dict.keys()):
                    if key >= point.y:
                        break
                    rock_points_dict.pop(key)
            height = max(height, point.y)
        heights.append(height)

        turtle_idx = 5
        hare_idx = 10
        while hare_idx < stopped_rocks and prev_movements[turtle_idx:turtle_idx+5] != prev_movements[hare_idx:hare_idx+5]:
            turtle_idx += 1
            hare_idx = turtle_idx * 2
        cycle_start = 0
        turtle_idx = 0
        while hare_idx < stopped_rocks and prev_movements[turtle_idx:turtle_idx+5] != prev_movements[hare_idx:hare_idx+5]:
            cycle_start += 5
            turtle_idx += 5
            hare_idx += 5

        if hare_idx < stopped_rocks:
            print(f"CYCLE!")
            cycle_length = hare_idx - turtle_idx
            height_diff = heights[hare_idx] - heights[turtle_idx]


            mult = stopped_rocks_target // cycle_length
            while (cycle_length * mult) > stopped_rocks_target:
                mult -= 1

            print(f"CYCLE @ {cycle_start}, len:{cycle_length}, h_diff: {height_diff}, mult: {mult}")

            gap = stopped_rocks_target - cycle_start - (cycle_length * mult)
            total_height = (height_diff * mult) + heights[cycle_start] + (heights[cycle_start+gap] - heights[cycle_start])
            return total_height + 1

        if stopped_rocks % 1_000_000 == 0:
            print(f"Rock {stopped_rocks}")

    if stopped_rocks_target < 10_000:
        print_rocks(rock_points_dict, height)#, to_std_out=True)
    return height + 1


def main() -> None:
    lines = []
    with file_input() as file:
        while line := file.readline():
            lines.append(line)
    height = simulate(lines[0])
    print(f"{height}")

    height = simulate(lines[0], 1_000_000_000_000)
    print(f"{height}")


if __name__ == "__main__":
    main()