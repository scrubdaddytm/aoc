from aoc.cli import file_input
from aoc.geometry import Point
from aoc.geometry import get_line


def get_overlaps(simple_lines: list[Point], support_45_deg=True) -> int:
    seen_points = dict()
    for line in simple_lines:
        for point in get_line(*line, support_45_deg=support_45_deg):
            count = seen_points.get(point, 0)
            count += 1
            seen_points[point] = count

    overlap_count = 0
    for point, count in seen_points.items():
        if count >= 2:
            overlap_count += 1
    return overlap_count


def main() -> None:
    lines = []
    with file_input() as file:
        while line := file.readline():
            start, end = (
                Point.from_list(list(map(int, point.split(","))))
                for point in line.strip().split(" -> ")
            )
            lines.append((start, end))

    print(f"part 1: overlap_count={get_overlaps(lines, False)}")
    print(f"part 2: overlap_count={get_overlaps(lines)}")


if __name__ == "__main__":
    main()
