from collections import defaultdict
from itertools import product

from aoc.cli import file_input
from aoc.geometry import ORIGIN, LineSegment, Point, down, left, right, up


def parse_wire(raw_wire: str) -> list[LineSegment]:
    origin = Point(0, 0)
    wire_points = [origin]
    wire = []
    for wire_segment in raw_wire.split(","):
        segment_start = wire_points[-1]

        direction = wire_segment[0]
        distance = int(wire_segment[1:])
        match direction:
            case "U":
                wire_points.append(up(segment_start, distance))
            case "D":
                wire_points.append(down(segment_start, distance))
            case "R":
                wire_points.append(right(segment_start, distance))
            case "L":
                wire_points.append(left(segment_start, distance))

        wire.append(LineSegment(wire_points[-2], wire_points[-1]))

    return wire


def find_intersections(
    wire_a: list[tuple[int, int]],
    wire_b: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    intersections = []

    for a, b in product(wire_a, wire_b):
        intersection = a.point_intersection(b)
        if intersection and intersection != ORIGIN:
            intersections.append(intersection)

    return intersections


def count_steps(
    wires: list[list[LineSegment]],
    intersections: list[Point],
) -> dict[Point, int]:
    step_count = defaultdict(int)

    for wire in wires:
        steps = 0
        uncounted = set(intersections)
        for line in wire:
            counted = set()
            for intersection in uncounted:
                if line.contains_point(intersection):
                    dist = line.a.distance(intersection)
                    step_count[intersection] += steps + dist
                    counted.add(intersection)

            uncounted -= counted
            steps += line.length

    return step_count


def main() -> None:
    first_wire = second_wire = None
    with file_input() as file:
        first_wire = parse_wire(file.readline().strip())
        second_wire = parse_wire(file.readline().strip())

    p1 = 0
    p2 = 0

    intersections = find_intersections(first_wire, second_wire)

    p1 = ORIGIN.distance(intersections[0])

    for intersection in intersections[1:]:
        p1 = min(p1, ORIGIN.distance(intersection))

    step_count = count_steps([first_wire, second_wire], intersections)
    p2 = min(step_count.values())

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
