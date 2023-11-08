from aoc.cli import file_input
from dataclasses import dataclass
from collections import deque


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

    def __repr__(self) -> str:
        return f"({self.x},{self.y})"

    def from_list(list_in: list[str]) -> "Point":
        return Point(int(list_in[0]), int(list_in[1]))


@dataclass(frozen=True)
class Line:
    a: Point
    b: Point

    def all_points(self) -> set[Point]:
        points = set([self.a, self.b])
        
        if self.a.x != self.b.x:
            x = self.a.x
            incr = -1 if self.a.x - self.b.x > 0 else 1
            while x != self.b.x:
                points.add(Point(x, self.a.y))
                x += incr

        if self.a.y != self.b.y:
            y = self.a.y
            incr = -1 if self.a.y - self.b.y > 0 else 1
            while y != self.b.y:
                points.add(Point(self.a.x, y))
                y += incr

        return points


def down(p: Point) -> Point:
    return Point(p.x, p.y+1)

def down_right(p: Point) -> Point:
    return Point(p.x+1, p.y+1)

def down_left(p: Point) -> Point:
    return Point(p.x-1, p.y+1)


def print_points(rocks: set[Point], sand: set[Point], grain: Point | None = None, floor: bool = False) -> None:
    all_x = [p.x for p in rocks | sand]
    all_y = [p.y for p in rocks]
    min_x, max_x = min(all_x), max(all_x)+1
    min_y, max_y = 0, max(all_y)+1

    if floor:
        max_y += 2

    grid = [["." for _ in range(max_x - min_x)] for _ in range(max_y)]
    for x in range(max_x - min_x):
        for y in range(max_y):
            p = Point(x+min_x, y+min_y)
            if p in rocks: 
                grid[y][x] = "#"
            elif p in sand:
                grid[y][x] = "o"

    grid[0][500-min_x] = "+"
    if grain:
        grid[grain.y][grain.x-min_x] = "0"

    if floor:
        for x in range(max_x - min_x):
            grid[max_y-1][x] = "#"

    print(f"{min_x} -> {max_x}")
    for y, row in enumerate(grid):
        print(f"{y:^3} {''.join(row)}")


def get_max_y_values(rock_points: set[Point]) -> tuple[dict[int, int], int]:
    max_y_values = {}
    for point in rock_points:
        max_y_values[point.x] = max(max_y_values.get(point.x, 0), point.y) 
    return max_y_values, max({p.y for p in rock_points})


def get_rock_points(rocks: list[list[Line]]) -> set[Point]:
    points = set()
    for lines in rocks:
        for line in lines:
            points |= line.all_points()
    return points


def drop_sand_round_two(rocks: set[Point]) -> int:
    sand = set()
    _, max_y = get_max_y_values(rocks)

    q = deque()
    q.append(Point(500, 0))
    while q:
        grain_of_sand = q.popleft()
        if grain_of_sand in sand or grain_of_sand.y == max_y + 2 or grain_of_sand in rocks:
            continue
        sand.add(grain_of_sand)
        if len(sand) % 1000 == 0:
            print_points(rocks, sand, grain_of_sand, floor=True)
        q.extend([down_left(grain_of_sand), down(grain_of_sand), down_right(grain_of_sand)])

    print_points(rocks, sand, floor=True)
    return len(sand)


def drop_all_sand(rocks: set[Point]) -> int:
    sand = set()

    max_y_values, _ = get_max_y_values(rocks)

    def drop_sand(grain_of_sand: Point) -> Point | None:
        if grain_of_sand.y > max_y_values.get(grain_of_sand.x, 0):
            raise ValueError(f"Done at {grain_of_sand}")
        elif grain_of_sand in rocks | sand:
            return None
        for direction in [down, down_left, down_right]:
            terminal_sand = drop_sand(direction(grain_of_sand))
            if terminal_sand:
                return terminal_sand
        return grain_of_sand
            
    while True:
        try:
            terminal_point = drop_sand(Point(500, 0))
            sand.add(terminal_point)
            if len(sand) % 1000 == 0:
                print_points(rocks, sand, terminal_point)
        except ValueError as e:
            print(e)
            break

    print_points(rocks, sand)
    return len(sand)


def main() -> None:
    raw_rocks = []
    with file_input() as file:
        while line := file.readline():
            sequence = [Point.from_list(p.split(',')) for p in line.strip().split(' -> ')]
            lines = []
            a = sequence[0]
            for b in sequence[1:]:
                lines.append(Line(a, b))
                a = b
            raw_rocks.append(lines)

    rocks = get_rock_points(raw_rocks)
    drop_count = drop_all_sand(rocks)
    print(f"ROUND 1: {drop_count=}")

    drop_count = drop_sand_round_two(rocks)
    print(f"ROUND 2: {drop_count=}")


if __name__ == "__main__":
    main()