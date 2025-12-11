from functools import cache
from itertools import pairwise

from aoc.cli import file_input


def main() -> None:
    devices = {}
    with file_input() as file:
        while line := file.readline().strip():
            device, outputs = line.split(": ")
            devices[device] = outputs.split(" ")

    @cache
    def paths(device, target="out") -> int:
        if device == target:
            return 1

        if device not in devices:
            return 0

        path_count = 0
        for output in devices[device]:
            path_count += paths(output, target)

        return path_count

    p1 = None
    if "you" in devices:
        p1 = paths("you")
    p2 = 0

    path_1 = ["svr", "dac", "fft", "out"]
    path_2 = ["svr", "fft", "dac", "out"]

    for path in [path_1, path_2]:
        running_count = 1
        for a, b in pairwise(path):
            path_count = paths(a, b)
            if not path_count:
                running_count = 0
                break
            running_count *= path_count
        p2 += running_count

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
