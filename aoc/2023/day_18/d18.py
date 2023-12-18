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
            instruction[2] = instruction[2][1:-1]
            instructions.append(instruction)

    a = Point(0, 0)
    a_p2 = a
    perimiter_area_p1 = 0
    corners_p1 = [a]
    perimiter_area_p2 = 0
    corners_p2 = [a]
    for instruction in instructions:
        direction = DIRECTIONS[instruction[0]](Point(0, 0))
        direction = Point(direction.x * instruction[1], direction.y * instruction[1])
        b = a.move(direction)
        corners_p1.append(b)
        perimiter_area_p1 += instruction[1]
        a = b

        p2_direction = DIRECTIONS[instruction[2][-1]](Point(0, 0))
        length = int(instruction[2][1:-1], 16)
        p2_direction = Point(p2_direction.x * length, p2_direction.y * length)
        b_p2 = a_p2.move(p2_direction)
        corners_p2.append(b_p2)
        perimiter_area_p2 += length
        a_p2 = b_p2

    for p, item in enumerate(((corners_p1, perimiter_area_p1), (corners_p2, perimiter_area_p2))):
        corners, perimiter_area = item
        area = 0
        for a, b in pairwise(reversed(corners)):
            area += determinant(a, b)
        area += determinant(corners[0], corners[-1])
        area //= 2
        area += perimiter_area // 2 + 1
        print(f"Part {p}: {area}")


if __name__ == "__main__":
    main()
