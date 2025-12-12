from collections.abc import Iterable
from enum import Enum
from typing import Any

from aoc.geometry import Point


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


def make_grid(
    points: dict[Point, Any],
    max_x: int | None = None,
    max_y: int | None = None,
    min_x: int | None = None,
    min_y: int | None = None,
    invert_y: bool = False,
    default_str: str = ".",
) -> str:
    if max_x is None:
        max_x = max(points.keys(), key=lambda p: p.x).x
    if max_y is None:
        max_y = max(points.keys(), key=lambda p: p.y).y
    if min_x is None:
        min_x = min(points.keys(), key=lambda p: p.x).x
    if min_y is None:
        min_y = min(points.keys(), key=lambda p: p.y).y
    print_str = []
    for y in range(min_y, max_y + 1):
        row = ""
        for x in range(min_x, max_x + 1):
            p = Point(x, y)
            if p in points:
                row += str(points[p])
            else:
                row += default_str
        print_str.append(row)
    if invert_y:
        print_str = reversed(print_str)
    return "\n".join(print_str)


def print_grid(
    points: dict[Point, str],
    max_x: int | None = None,
    max_y: int | None = None,
    min_x: int | None = None,
    min_y: int | None = None,
    invert_y: bool = False,
    default_str: str = ".",
):
    grid = make_grid(points, max_x, max_y, min_x, min_y, invert_y, default_str)
    print(grid)


def print_point_grid(
    points: Iterable[Point],
    max_x: int | None = None,
    max_y: int | None = None,
    min_x: int | None = None,
    min_y: int | None = None,
    invert_y: bool = False,
) -> None:
    if not points:
        return
    points = {p: "#" for p in points}
    print_grid(points, max_x, max_y, min_x, min_y, invert_y)
