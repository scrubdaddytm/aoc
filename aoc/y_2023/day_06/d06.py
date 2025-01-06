from aoc.cli import file_input
import math


def main() -> None:
    rounds = []
    r2_time = 0
    r2_distance = 0
    with file_input() as file:
        time = list(map(int, file.readline().strip().split(":")[1].split()))
        distance = list(map(int, file.readline().strip().split(":")[1].split()))
        r2_time = int("".join(map(str, time)))
        r2_distance = int("".join(map(str, distance)))
        rounds = list(zip(time, distance))

    better_time_count = []
    for time, distance in rounds:
        print(f"{time=}, {distance=}")
        better_times = 0
        for ms in range(1, time):
            d_traveled = ms * (time - ms)
            if d_traveled > distance:
                better_times += 1
        print(f"  {better_times=}")
        better_time_count.append(better_times)

    print(f"Part 1: {math.prod(better_time_count)}")

    print(f"{r2_time=}, {r2_distance=}")
    better_times = 0
    for ms in range(1, r2_time):
        d_traveled = ms * (r2_time - ms)
        if d_traveled > r2_distance:
            better_times += 1

    print(f"Part 2: {better_times}")


if __name__ == "__main__":
    main()
