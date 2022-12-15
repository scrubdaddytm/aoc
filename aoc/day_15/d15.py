from aoc.cli import file_input
from dataclasses import dataclass
from aoc.geometry import Point
from aoc.geometry import distance
from aoc.geometry import up, down, left, right
from collections import deque
import re


@dataclass
class Sensor:
    location: Point
    beacon: Point

    def intersects(p: Point) -> bool:
        pass

def print_map(sensors: set[Point], beacons: set[Point], coverage: set[Point] | None = None) -> None:
    if not coverage:
        coverage = set()
    all_x = set([p.x for p in (beacons | sensors)])
    all_y = set([p.y for p in (beacons | sensors)])

    min_x, max_x = min(all_x), max(all_x)+1
    min_y, max_y = min(all_y), max(all_y)+1

    grid = [["." for _ in range(max_x - min_x)] for _ in range(max_y - min_y)]
    for x in range(max_x - min_x):
        for y in range(max_y - min_y):
            p = Point(x+min_x, y+min_y)
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
        for idx in range(min_x, len(row_chars)-big_x_char_count-1):
            if idx % 5 == 0 and len(str(idx)) >= big_x_char_count - row:
                digit = idx
                for _ in range(row, big_x_char_count-1):
                    digit //= 10
                row_chars[idx+big_y_char_count+1+abs(min_x)] = str(digit%10)
        print(f"{''.join(row_chars)}")
            
        
    y_idx = min_y
    for line in grid:
        print(f"{y_idx:2} {''.join(line)}")
        y_idx += 1


def calculate_coverage(sensors: list[Sensor], beacons: set[Point], sensor_locs: set[Point], row: int = 10) -> int:
    row_coverage = set()

    for sensor in sensors:
        dist = distance(sensor.location, sensor.beacon)
        print(f"==== S:{sensor.location}, B:{sensor.beacon}, d:{dist} ====")

    return len(row_coverage)


def main() -> None:
    sensors = []
    sensor_locs = []
    beacons = []
    with file_input() as file:
        pattern = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")
        while line := file.readline():
            m = pattern.match(line)
            sensor_locs.append(Point(int(m.group(1)), int(m.group(2))))
            beacons.append(Point(int(m.group(3)), int(m.group(4))))
            sensors.append(Sensor(sensor_locs[-1], beacons[-1])) 

    beacons = set(beacons)
    sensor_locs = set(sensor_locs)
    # print_map(sensor_locs, beacons)
    coverage_count = calculate_coverage(sensors, beacons, sensor_locs, row=2_000_000)
    print(f"{coverage_count=}")




if __name__ == "__main__":
    main()


    r"Sensor at x=(\d+), y=(\d+): closest beacon is at x=(\d+), y=(\d+)"