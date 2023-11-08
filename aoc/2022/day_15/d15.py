from aoc.cli import file_input
import argparse
from dataclasses import dataclass
from aoc.geometry import Point
from aoc.geometry import distance
from aoc.geometry import up, down, left, right
from collections import deque
import re
from typing import Optional


@dataclass
class Sensor:
    location: Point
    beacon: Point

    def intersects(p: Point) -> bool:
        pass


@dataclass(frozen=True, order=True)
class LineSegment:
    a: Point
    b: Point

    def __repr__(self) -> str:
        return f"{self.a}->{self.b}"

    def x_intersection(self, other: "LineSegment") -> Optional["LineSegment"]:
        left = max(self.a.x, other.a.x)
        right = min(self.b.x, other.b.x)
        if left > right:
            return None
        return LineSegment(Point(left, self.a.y), Point(right, self.a.y))

    def remove_x_segment(self, other: "LineSegment", max_coord: int) -> list["LineSegment"]:
        if self == other:
            return []
        elif self.a.x <= other.a.x and other.b.x <= self.b.x:  # CONTAINS
            segments = []
            # if self.a.x == other.a.x:
            #     pass
            # elif self.b.x == other.b.x:
            #     pass

            if 0 <= other.a.x - 1 <= max_coord and self.a.x <= other.a.x - 1:
                segments.append(LineSegment(self.a, Point(other.a.x - 1, other.a.y)))
            if 0 <= other.a.x + 1 <= max_coord and other.b.x + 1 <= self.b.x:
                segments.append(LineSegment(Point(other.b.x + 1, other.b.y), self.b))
            return segments

        elif self.b.x == other.a.x:  # INTERSECTS AT B', A"
            if 0 <= self.a.x - 1 <= max_coord and self.a.x <= self.b.x - 1:
                return [LineSegment(self.a, Point(self.b.x - 1, self.b.y))]
            return []
        elif self.a.x == other.b.x:  # INTERSECTS AT B", A'
            if 0 <= self.a.x + 1 <= max_coord and self.a.x + 1 <= self.b.x:
                return [LineSegment(Point(self.a.x + 1, self.a.y)), self.b]
            return []
        elif self.a.x < other.a.x:  # OVERLAPS AT A", B'
            if 0 <= other.a.x - 1 <= max_coord and self.a.x <= other.a.x - 1:
                return [LineSegment(self.a, Point(other.a.x - 1, other.a.y))]
            return []
        elif other.a.x > self.a.x:  # OVERLAPS AT
            if 0 <= other.a.x + 1 <= max_coord and other.b.x + 1 <= self.b.x:
                return [LineSegment(Point(other.b.x + 1, other.b.y), self.b)]
        return [self]


def print_map(sensors: set[Point], beacons: set[Point], coverage: set[Point] | None = None) -> None:
    if not coverage:
        coverage = set()
    all_x = set([p.x for p in (beacons | sensors)])
    all_y = set([p.y for p in (beacons | sensors)])

    min_x, max_x = min(all_x), max(all_x) + 1
    min_y, max_y = min(all_y), max(all_y) + 1

    grid = [["." for _ in range(max_x - min_x)] for _ in range(max_y - min_y)]
    for x in range(max_x - min_x):
        for y in range(max_y - min_y):
            p = Point(x + min_x, y + min_y)
            if p in beacons:
                grid[y][x] = "B"
            elif p in sensors:
                grid[y][x] = "S"
            elif p in coverage:
                grid[y][x] = "#"

    big_x_char_count = len(str(max(abs(min_x), abs(max_x))))
    big_y_char_count = len(str(max(abs(min_y), abs(max_y))))

    print(f"{big_x_char_count=}")
    for row in range(big_x_char_count):
        row_chars = [" " for _ in range(max_x - min_x + 1 + big_y_char_count + 1)]
        for idx in range(min_x, len(row_chars) - big_x_char_count - 1):
            if idx % 5 == 0 and len(str(idx)) >= big_x_char_count - row:
                digit = idx
                for _ in range(row, big_x_char_count - 1):
                    digit //= 10
                row_chars[idx + big_y_char_count + 1 + abs(min_x)] = str(digit % 10)
        print(f"{''.join(row_chars)}")

    y_idx = min_y
    for line in grid:
        print(f"{y_idx:2} {''.join(line)}")
        y_idx += 1


def subtract_line(lines: list[LineSegment], operand: LineSegment, max_coord: int) -> list[LineSegment]:
    new_lines = []
    for line in lines:
        intersection = line.x_intersection(operand)
        if intersection == line:
            continue
        elif intersection:
            new_lines.extend(line.remove_x_segment(intersection, max_coord))
        else:
            new_lines.append(line)

    sanitized_lines = set()
    if new_lines:
        l = new_lines[0]
        for idx in range(1, len(new_lines)):
            if l.b == new_lines[idx].a:
                l = LineSegment(l.a, new_lines[idx].b)
                sanitized_lines.add(l)
            else:
                sanitized_lines.add(l)
                l = new_lines[idx]
        sanitized_lines.add(l)
    return sorted(sanitized_lines)


def find_distress_beacon(sensors: list[Sensor], beacons: set[Point], sensor_locs: set[Point], max_coord: int = 20) -> Point:
    missing_coverage = {}

    for sensor in sensors:
        dist = distance(sensor.location, sensor.beacon)

        for y in range(max(0, sensor.location.y - dist), min(max_coord, sensor.location.y + dist) + 1):
            row_lines = missing_coverage.get(y, [LineSegment(Point(0, y), Point(max_coord, y))])
            if not row_lines:
                continue
            x_dist = dist - abs(y - sensor.location.y)

            circle_slice = LineSegment(
                Point(max(0, sensor.location.x - x_dist), y), Point(min(max_coord, sensor.location.x + x_dist), y)
            )
            missing_coverage[y] = subtract_line(row_lines, circle_slice, max_coord)
        print(f"==== S:{sensor.location}, B:{sensor.beacon}, d:{dist} ====")

    point = None
    for idx, line in missing_coverage.items():
        if line:
            point = line[0].a
            print(f"{idx} -> {line}")
    return (point.x * 4_000_000) + point.y if point else None


def calculate_coverage(sensors: list[Sensor], beacons: set[Point], sensor_locs: set[Point], row: int = 10) -> int:
    row_coverage = set()

    for sensor in sensors:
        dist = distance(sensor.location, sensor.beacon)

        if row < (sensor.location.y - dist) or row > (sensor.location.y + dist):
            continue

        x_dist = dist - abs(row - sensor.location.y)
        print(f"{sensor.location.x-x_dist} -> {sensor.location.x+x_dist}")
        for x in range(sensor.location.x - x_dist, sensor.location.x + x_dist + 1):
            row_coverage.add(Point(x, row))

        print(f"==== S:{sensor.location}, B:{sensor.beacon}, d:{dist}, coverage_count:{len(row_coverage)} ====")

    return len(row_coverage - beacons)


def main() -> None:
    sensors = []
    sensor_locs = []
    beacons = []
    row = 10
    max_coord = 20
    with file_input() as file:
        if file.name == "aoc/day_15/d15.in":
            row = 2_000_000
            max_coord = 4_000_000
        pattern = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
        while line := file.readline():
            m = pattern.match(line)
            sensor_locs.append(Point(int(m.group(1)), int(m.group(2))))
            beacons.append(Point(int(m.group(3)), int(m.group(4))))
            sensors.append(Sensor(sensor_locs[-1], beacons[-1]))

    beacons = set(beacons)
    sensor_locs = set(sensor_locs)
    coverage_count = calculate_coverage(sensors, beacons, sensor_locs, row=row)
    print(f"{coverage_count=}")

    frequency = find_distress_beacon(sensors, beacons, sensor_locs, max_coord=max_coord)
    print(f"{frequency=}")


if __name__ == "__main__":
    main()

    r"Sensor at x=(\d+), y=(\d+): closest beacon is at x=(\d+), y=(\d+)"
