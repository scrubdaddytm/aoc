from aoc.cli import file_input
from dataclasses import dataclass


@dataclass
class Lanternfish:
    timer: int = 8


def main() -> None:
    fish = []
    with file_input() as file:
        while line := file.readline():
            fish = [Lanternfish(int(val)) for val in line.strip().split(",")]

    for _ in range(80):
        new_fish = []
        for f in fish:
            if f.timer == 0:
                f.timer = 6
                new_fish.append(Lanternfish())
            else:
                f.timer -= 1
        fish.extend(new_fish)
    print(f"part 1: {len(fish)}")


if __name__ == "__main__":
    main()
