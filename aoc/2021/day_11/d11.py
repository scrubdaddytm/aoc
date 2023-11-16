from aoc.cli import file_input
from aoc.geometry import Point, in_bounds, DIRECTIONS
from aoc.print_tools import Color


def print_octopuses(octopuses: list[list[int]]) -> None:
    print_str = ""
    for row in octopuses:
        for octopus in row:
            if octopus == 0:
                print_str += Color.GREEN + "0" + Color.END
            else:
                print_str += str(octopus)
        print_str += "\n"
    print(print_str)


def main() -> None:
    octopuses = []
    with file_input() as file:
        while line := file.readline().strip():
            octopuses.append(list(map(int, list(line))))
    print("Before any steps:")
    print_octopuses(octopuses)

    p1_total_flashes = 0
    step = 0
    synchronized = False
    while not synchronized:
        step += 1
        flashers = []
        flashed = set()
        for y in range(10):
            for x in range(10):
                octopuses[y][x] += 1
                if octopuses[y][x] > 9:
                    flashers.append(Point(x, y))

        while flashers:
            flasher = flashers.pop()
            if flasher in flashed:
                continue
            flashed.add(flasher)
            for direction in DIRECTIONS:
                next_octopus = direction(flasher)
                if in_bounds(next_octopus, 10, 10) and next_octopus not in flashed:
                    octopuses[next_octopus.y][next_octopus.x] += 1
                    if octopuses[next_octopus.y][next_octopus.x] > 9:
                        flashers.append(next_octopus)

        if step < 101:
            p1_total_flashes += len(flashed)

        for flasher in flashed:
            octopuses[flasher.y][flasher.x] = 0

        if step <= 10 or step % 10 == 0:
            print(f"After step {step}:")
            print_octopuses(octopuses)

        if len(flashed) == 100:
            synchronized = True

    print(f"part 1: {p1_total_flashes=}")
    print(f"part 2: sycnrhonized on {step=}")


if __name__ == "__main__":
    main()
