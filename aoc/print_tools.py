from enum import Enum
from aoc.geometry import Point
from collections.abc import Iterable


class Color(str, Enum):
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def print_point_grid(
    points: Iterable[Point],
    max_x: int | None = None,
    max_y: int | None = None,
    min_x: int | None = None,
    min_y: int | None = None,
) -> None:
    points = set(points)
    if not max_x:
        max_x = max(points, key=lambda p: p.x).x
    if not max_y:
        max_y = max(points, key=lambda p: p.y).y
    if not min_x:
        min_x = min(points, key=lambda p: p.x).x
    if not min_y:
        min_y = min(points, key=lambda p: p.y).y
    print(f"{min_x=},{min_y=} -> {max_x=},{max_y=}")
    print_str = ""
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if Point(x, y) in points:
                print_str += "#"
            else:
                print_str += "."
        print_str += "\n"
    print(print_str.strip())
