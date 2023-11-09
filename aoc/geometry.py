from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

    def __repr__(self) -> str:
        return f"({self.x},{self.y})"

    def from_list(list_in: list[str]) -> "Point":
        return Point(int(list_in[0]), int(list_in[1]))

    def distance(self, b: "Point") -> int:
        return abs(self.x - b.x) + abs(self.y - b.y)


def up(p: Point, dist: int = 1) -> Point:
    return Point(p.x, p.y + dist)


def up_right(p: Point) -> Point:
    return Point(p.x + 1, p.y + 1)


def up_left(p: Point) -> Point:
    return Point(p.x - 1, p.y + 1)


def down(p: Point, dist: int = 1) -> Point:
    return Point(p.x, p.y - dist)


def down_left(p: Point) -> Point:
    return Point(p.x - 1, p.y - 1)


def down_right(p: Point) -> Point:
    return Point(p.x + 1, p.y - 1)


def left(p: Point, dist: int = 1) -> Point:
    return Point(p.x - dist, p.y)


def right(p: Point, dist: int = 1) -> Point:
    return Point(p.x + dist, p.y)


def distance(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def get_line(a: Point, b: Point) -> list[Point]:
    if a.x == b.x:
        return [Point(a.x, new_y) for new_y in range(min(a.y, b.y), max(a.y, b.y) + 1)]
    elif a.y == b.y:
        return [Point(new_x, a.y) for new_x in range(min(a.x, b.x), max(a.x, b.x) + 1)]
    else:
        return []  # this might be needed someday
