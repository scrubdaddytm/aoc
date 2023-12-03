import string
from collections import defaultdict

from aoc.cli import file_input
from aoc.geometry import Point
from aoc.geometry import in_bounds
from aoc.geometry import DIRECTIONS


DIGITS = set(string.digits)
NOT_SYMBOLS = DIGITS | set(["."])


def main() -> None:
    lines = []
    with file_input() as file:
        while line := file.readline().strip():
            lines.append(line)

    part_points = set()
    part_numbers = []
    gears = defaultdict(list)

    for y, row in enumerate(lines):
        for x, char in enumerate(row):
            current_point = Point(x, y)
            if char == "." or char not in NOT_SYMBOLS or current_point in part_points:
                continue
            for direction in DIRECTIONS:
                to_check = direction(current_point)
                if not in_bounds(to_check, max_x=len(row), max_y=len(lines)):
                    continue
                if lines[to_check.y][to_check.x] not in NOT_SYMBOLS:
                    num_start = num_end = x
                    while num_start - 1 >= 0 and row[num_start - 1] in DIGITS:
                        num_start -= 1
                    while num_end + 1 < len(row) and row[num_end + 1] in DIGITS:
                        num_end += 1
                    part_number = int(row[num_start : num_end + 1])
                    part_numbers.append(part_number)
                    if lines[to_check.y][to_check.x] == "*":
                        gears[to_check].append(part_number)
                    for point_x in range(num_start, num_end + 1):
                        part_points.add(Point(point_x, y))

    print(f"part 1: {sum(part_numbers)}")
    gear_ratio_sum = 0
    for parts in gears.values():
        if len(parts) == 2:
            gear_ratio_sum += parts[0] * parts[1]
    print(f"part 2: {gear_ratio_sum}")


if __name__ == "__main__":
    main()
