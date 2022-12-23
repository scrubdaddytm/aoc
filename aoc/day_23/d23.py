from aoc.cli import file_input
from dataclasses import dataclass
from aoc.geometry import Point
from aoc.geometry import up
from aoc.geometry import up_right
from aoc.geometry import up_left
from aoc.geometry import down
from aoc.geometry import down_right
from aoc.geometry import down_left
from aoc.geometry import left
from aoc.geometry import right
from itertools import cycle
from copy import deepcopy


def north_dirs(p: Point) -> set[Point]:
    return set(
        [
            down(p),
            down_left(p),
            down_right(p),
        ]
    )


def south_dirs(p: Point) -> set[Point]:
    return set(
        [
            up(p),
            up_left(p),
            up_right(p),
        ]
    )


def east_dirs(p: Point) -> set[Point]:
    return set(
        [
            right(p),
            up_right(p),
            down_right(p),
        ]
    )


def west_dirs(p: Point) -> set[Point]:
    return set(
        [
            left(p),
            up_left(p),
            down_left(p),
        ]
    )


def all_dirs(p: Point) -> set[Point]:
    return set(
        [
            up(p),
            down(p),
            left(p),
            right(p),
            down_left(p),
            down_right(p),
            up_left(p),
            up_right(p),
        ]
    )


DIR_FUNCS = {
    "n": (north_dirs, down),
    "s": (south_dirs, up),
    "w": (west_dirs, left),
    "e": (east_dirs, right),
}


def print_map(elves: set[Point]) -> None:
    xs = [elf.x for elf in elves]
    min_x, max_x = min(xs), max(xs)
    ys = [elf.y for elf in elves]
    min_y, max_y = min(ys), max(ys)

    x_diff = max_x - min_x
    y_diff = max_y - min_y

    for y in range(min_y, max_y + 1):
        row = ""
        for x in range(min_x, max_x + 1):
            if Point(x, y) in elves:
                row += "#"
            else:
                row += "."
        print(row)
    print()


def simulate(elves: set[Point], rounds: int | None = None) -> int:
    order = ["n", "s", "w", "e"]
    print_map(elves)

    rnd = 1
    while True:
        print(rnd)
        print_map(elves)
        if rounds and rnd == rounds:
            break
        proposals = {}
        for elf in elves:
            if not all_dirs(elf) & elves:
                continue
            for idx in range(4):
                dir_fs = DIR_FUNCS[order[(rnd-1 + idx) % 4]]
                if not dir_fs[0](elf) & elves:
                    prop = dir_fs[1](elf)
                    props = proposals.get(prop, [])
                    props.append(elf)
                    proposals[prop] = props
                    break

        if len(proposals.keys()) == 0:
            break
        for pos, proposers in proposals.items():
            if len(proposers) == 1:
                elves.remove(proposers[0])
                elves.add(pos)
        rnd += 1

    if rounds:
        xs = [elf.x for elf in elves]
        min_x, max_x = min(xs), max(xs)
        ys = [elf.y for elf in elves]
        min_y, max_y = min(ys), max(ys)

        area = abs(max_x - min_x + 1) * abs(max_y - min_y + 1)
        return area - len(elves)
    return rnd

def main() -> None:
    elves = set()
    with file_input() as file:
        y = 0
        while line := file.readline():
            for x, char in enumerate(line):
                if char == "#":
                    elves.add(Point(x, y))
            y += 1
    print(f"Round 1: {simulate(deepcopy(elves), 10)}")
    print(f"Round 1: {simulate(deepcopy(elves))}")


if __name__ == "__main__":
    main()
