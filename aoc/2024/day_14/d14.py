import re
from collections import Counter
from math import prod

from aoc.cli import file_input
from aoc.geometry import Point
from aoc.print_tools import print_grid


def move_robot(
    robot: Point, velocity: Point, x_bound: int, y_bound: int, seconds: int = 100
):
    move = Point(velocity.x * seconds, velocity.y * seconds)
    end_robot = robot.move(move)
    return Point(end_robot.x % x_bound, end_robot.y % y_bound)


def main() -> None:
    robots = []
    with file_input() as file:
        while line := file.readline().strip():
            px, py, vx, vy = map(int, re.findall(r"(\-?\d+)", line))
            robots.append((Point(px, py), Point(vx, vy)))

    print_grid(Counter([r[0] for r in robots]))
    print()

    sample = False

    x_bound = 0
    y_bound = 0
    if sample:
        x_bound = 11
        y_bound = 7
    else:
        x_bound = 101
        y_bound = 103
    mid_x = x_bound // 2
    mid_y = y_bound // 2

    state = Counter()
    quadrants = Counter()
    for robot, velocity in robots:
        print(f"{robot=}, {velocity=}")
        moved_robot = move_robot(robot, velocity, x_bound, y_bound, 100)
        state[moved_robot] += 1
        if moved_robot.x < mid_x and moved_robot.y < mid_y:
            quadrants[0] += 1
        elif moved_robot.x < mid_x and moved_robot.y > mid_y:
            quadrants[1] += 1
        elif moved_robot.x > mid_x and moved_robot.y < mid_y:
            quadrants[2] += 1
        elif moved_robot.x > mid_x and moved_robot.y > mid_y:
            quadrants[3] += 1

    print_grid(
        state,
        min_x=0,
        min_y=0,
        max_x=x_bound - 1,
        max_y=y_bound - 1,
    )
    print(quadrants)

    # gross
    for s in range(10000):
        state = Counter()
        for robot, velocity in robots:
            moved_robot = move_robot(robot, velocity, x_bound, y_bound, s)
            state[moved_robot] += 1
        print(f"TIME: {s}")
        print_grid(
            state,
            min_x=0,
            min_y=0,
            max_x=x_bound - 1,
            max_y=y_bound - 1,
        )

    p1 = prod(quadrants.values())
    p2 = 0

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
