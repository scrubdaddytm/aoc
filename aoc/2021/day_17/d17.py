import re
from aoc.cli import file_input
from aoc.geometry import Point, Rectangle
from aoc.print_tools import print_grid
from aoc.math import sum_of_series


def main() -> None:
    input_pattern = re.compile(r"-?\d+")
    target_zone = None
    with file_input() as file:
        while line := file.readline().strip():
            match = input_pattern.findall(line)
            target_zone = Rectangle(
                top_left=Point(int(match[0]), int(match[3])),
                bottom_right=Point(int(match[1]), int(match[2])),
            )

    print(f"{target_zone=}")

    # sample_input_velocities = [
    #     Point(7, 2),
    #     Point(6, 3),
    #     Point(9, 0),
    #     Point(17, -4),
    #     Point(6, 9),
    # ]
    possible_x = 1
    while target_zone.top_left.x > sum_of_series(possible_x):
        possible_x += 1
    if (
        not target_zone.top_left.x
        <= sum_of_series(possible_x)
        <= target_zone.bottom_right.x
    ):
        raise ValueError("um, this X calc didnt work")
    test_velocities = [Point(possible_x, abs(target_zone.bottom_right.y) - 1)]
    for initial_velocity in test_velocities:
        print("-" * 50)
        probe_start = Point(0, 0)

        probe = probe_start
        probe_locations = [probe]

        velocity = initial_velocity
        winner = False
        while probe.y >= target_zone.bottom_right.y:
            if probe in target_zone:
                winner = True
                break
            probe = probe.move(velocity)
            probe_locations.append(probe)
            velocity = Point(max(0, velocity.x - 1), velocity.y - 1)

        points = {}
        for point in target_zone.all_points():
            points[point] = "T"
        for location in probe_locations:
            points[location] = "#"
        points[probe_start] = "S"

        print_grid(points, invert_y=True)
        print(
            f"{winner=}, {initial_velocity=}, {probe=}, max y={max(p.y for p in probe_locations)}"
        )


if __name__ == "__main__":
    main()
