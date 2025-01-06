from aoc.cli import file_input
from dataclasses import dataclass


def surface_area(l, w, h) -> int:
    return 2 * l * w + 2 * w * h + 2 * h * l


def smallest_side_area(l, w, h) -> int:
    return min(l * w, w * h, h * l)


def ribbon_length(l, w, h) -> int:
    ordered_len = sorted([l, w, h])
    return 2 * ordered_len[0] + 2 * ordered_len[1] + (l * w * h)


def main() -> None:
    lines = []
    with file_input() as file:
        while line := file.readline():
            lines.append(tuple(map(int, line.split("x"))))

    surface_area_sum = 0
    ribbon_length_sum = 0
    for l, w, h in lines:
        surface_area_sum += surface_area(l, w, h) + smallest_side_area(l, w, h)
        ribbon_length_sum += ribbon_length(l, w, h)

    print(f"Part 1: {surface_area_sum}")
    print(f"Part 2: {ribbon_length_sum}")


if __name__ == "__main__":
    main()
