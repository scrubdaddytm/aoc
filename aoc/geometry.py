from dataclasses import dataclass

@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

    def __repr__(self) -> str:
        return f"({self.x},{self.y})"

    def from_list(list_in: list[str]) -> "Point":
        return Point(int(list_in[0]), int(list_in[1]))


def up(p: Point) -> Point:
    return Point(p.x, p.y+1)

def down(p: Point) -> Point:
    return Point(p.x, p.y-1)

def left(p: Point) -> Point:
    return Point(p.x-1, p.y)

def right(p: Point) -> Point:
    return Point(p.x+1, p.y)

def down_left(p: Point) -> Point:
    return Point(p.x-1, p.y-1)

def down_right(p: Point) -> Point:
    return Point(p.x+1, p.y-1)

def distance(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)