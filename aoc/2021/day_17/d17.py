import re
from aoc.cli import file_input
from aoc.geometry import Point, Rectangle
from aoc.math import sum_of_series
from itertools import product


SAMPLE_VALID_VELOCITIES = set(
    [
        Point(23, -10),
        Point(25, -7),
        Point(8, 0),
        Point(26, -10),
        Point(20, -8),
        Point(25, -6),
        Point(25, -10),
        Point(8, 1),
        Point(24, -10),
        Point(7, 5),
        Point(23, -5),
        Point(27, -10),
        Point(8, -2),
        Point(24, -5),
        Point(28, -7),
        Point(21, -6),
        Point(14, -3),
        Point(25, -8),
        Point(23, -7),
        Point(27, -6),
        Point(7, 4),
        Point(6, 5),
        Point(13, -3),
        Point(21, -5),
        Point(29, -5),
        Point(27, -7),
        Point(6, 3),
        Point(14, -4),
        Point(30, -10),
        Point(26, -8),
        Point(24, -6),
        Point(22, -10),
        Point(26, -9),
        Point(22, -9),
        Point(29, -7),
        Point(6, 6),
        Point(6, 9),
        Point(9, 0),
        Point(29, -10),
        Point(6, 1),
        Point(20, -7),
        Point(22, -5),
        Point(12, -3),
        Point(6, 0),
        Point(12, -4),
        Point(26, -5),
        Point(14, -2),
        Point(7, 9),
        Point(20, -6),
        Point(21, -7),
        Point(20, -5),
        Point(6, 4),
        Point(6, 2),
        Point(15, -3),
        Point(28, -9),
        Point(23, -9),
        Point(11, -4),
        Point(10, -1),
        Point(20, -9),
        Point(21, -10),
        Point(24, -9),
        Point(21, -7),
        Point(20, -5),
        Point(6, 4),
        Point(6, 2),
        Point(15, -3),
        Point(28, -9),
        Point(23, -9),
        Point(11, -4),
        Point(10, -1),
        Point(20, -9),
        Point(21, -10),
        Point(24, -9),
        Point(22, -6),
        Point(11, -2),
        Point(6, 7),
        Point(21, -9),
        Point(29, -9),
        Point(12, -2),
        Point(7, 1),
        Point(28, -6),
        Point(9, -1),
        Point(11, -1),
        Point(28, -5),
        Point(22, -7),
        Point(29, -6),
        Point(6, 8),
        Point(20, -10),
        Point(8, -1),
        Point(28, -8),
        Point(15, -2),
        Point(26, -7),
        Point(7, 6),
        Point(7, 0),
        Point(10, -2),
        Point(30, -7),
        Point(21, -8),
        Point(24, -7),
        Point(27, -5),
        Point(25, -5),
        Point(29, -8),
        Point(7, 7),
        Point(7, 3),
        Point(9, -2),
        Point(11, -3),
        Point(13, -4),
        Point(30, -8),
        Point(28, -10),
        Point(27, -9),
        Point(30, -9),
        Point(30, -5),
        Point(25, -9),
        Point(26, -6),
        Point(30, -6),
        Point(7, -1),
        Point(13, -2),
        Point(15, -4),
        Point(7, 8),
        Point(22, -8),
        Point(23, -8),
        Point(23, -6),
        Point(24, -8),
        Point(7, 2),
        Point(27, -8),
    ]
)


def get_x_series(x: int, max_x: int) -> list[int]:
    series = [x]
    idx = 0
    while series[idx] < max_x:
        if x > 0:
            x -= 1
        series.append(series[idx] + x)
        idx += 1
    while series[-1] > max_x:
        series.pop()
    return series


def get_neg_y_series(y: int, min_y: int) -> list[int]:
    series = [y]
    idx = 0
    while series[idx] > min_y:
        y -= 1
        series.append(series[idx] + y)
        idx += 1
    while series[-1] < min_y:
        series.pop()
    return series


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

    smallest_x = 1
    valid_x = []
    always_valid_x = []
    while target_zone.top_left.x > sum_of_series(smallest_x):
        smallest_x += 1
    while (
        target_zone.top_left.x
        <= sum_of_series(smallest_x)
        <= target_zone.bottom_right.x
    ):
        valid_x.append(smallest_x)
        always_valid_x.append(smallest_x)
        smallest_x += 1

    for x_option in range(smallest_x, target_zone.top_left.x):
        x_series = get_x_series(x_option, target_zone.bottom_right.x)
        if target_zone.top_left.x <= x_series[-1] <= target_zone.bottom_right.x:
            valid_x.append(x_option)

    valid_x.extend(
        [x for x in range(target_zone.top_left.x, target_zone.bottom_right.x + 1)]
    )

    valid_y = []
    for y_option in range(target_zone.bottom_right.y, abs(target_zone.bottom_right.y)):
        y_series = get_neg_y_series(y_option, target_zone.bottom_right.y)
        if target_zone.top_left.y >= y_series[-1] >= target_zone.bottom_right.y:
            valid_y.append(y_option)

    print(f"{valid_x=}")
    print(f"{valid_y=}")

    valid_velocities = target_zone.all_points()

    for pair in product(valid_x, valid_y):
        init_velocity = Point(pair[0], pair[1])
        if init_velocity in valid_velocities:
            continue
        velocity = init_velocity
        probe = Point(0, 0)
        while probe.y >= target_zone.bottom_right.y:
            if probe in target_zone:
                valid_velocities.add(init_velocity)
                break
            probe = probe.move(velocity)
            velocity = Point(max(0, velocity.x - 1), velocity.y - 1)

    # v grateful they told you what all the right values were
    # print(f"{SAMPLE_VALID_VELOCITIES - valid_velocities}")
    # print(f"{valid_velocities - SAMPLE_VALID_VELOCITIES}")

    max_y = max(p.y for p in valid_velocities)
    print(f"{max_y=} goes up to {sum_of_series(max_y)}")
    print(f"valid velocities = {len(valid_velocities)}")


if __name__ == "__main__":
    main()
