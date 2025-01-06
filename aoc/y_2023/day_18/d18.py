from itertools import pairwise
from aoc.cli import file_input
from aoc.geometry import Point, up, down, right, left, determinant


DIRECTIONS = {
    "R": right,
    "L": left,
    "U": up,
    "D": down,
    "0": right,
    "1": down,
    "2": left,
    "3": up,
}


def main() -> None:
    instructions = []
    with file_input() as file:
        while instruction := file.readline().strip():
            instruction = instruction.split()
            instruction[1] = int(instruction[1])
            instruction[2] = instruction[2][2:-1]
            instructions.append(instruction)

    perimeter_area_p1 = 0
    corners_p1 = [Point(0, 0)]
    perimeter_area_p2 = 0
    corners_p2 = [Point(0, 0)]
    for instruction in instructions:
        for direction, length, corners, perimeter_area in [
            (DIRECTIONS[instruction[0]](Point(0, 0)), instruction[1], corners_p1, perimeter_area_p1),
            (DIRECTIONS[instruction[2][-1]](Point(0, 0)), int(instruction[2][:-1], 16), corners_p2, perimeter_area_p2),
        ]:
            direction = Point(direction.x * length, direction.y * length)
            b = corners[-1].move(direction)
            corners.append(b)
            perimeter_area += length

    for p, item in enumerate(((corners_p1, perimeter_area_p1), (corners_p2, perimeter_area_p2))):
        corners, perimeter_area = item
        area = 0
        for a, b in pairwise(reversed(corners)):
            area += determinant(a, b)
        area += determinant(corners[0], corners[-1])
        area //= 2
        area += perimeter_area // 2 + 1
        print(f"Part {p}: {area}")


if __name__ == "__main__":
    main()
