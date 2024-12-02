from aoc.cli import file_input
from dataclasses import dataclass


def is_increasing_or_decreasing(levels: list[int]) -> bool:
    increasing = False
    decreasing = False
    prev = levels[0]
    for l in levels[1:]:
        if prev < l:
            increasing = True
        elif prev > l:
            decreasing = True
        if increasing and decreasing:
            return False
        prev = l
    return increasing or decreasing


def is_gradual(levels: list[int]) -> bool:
    prev = levels[0]
    for l in levels[1:]:
        diff = abs(prev - l)
        if diff == 0 or diff > 3:
            return False
        prev = l
    return True


def main() -> None:
    lines = []
    with file_input() as file:
        while line := file.readline():
            lines.append(list(map(int, line.split())))

    safe = 0
    safe_damp = 0
    for levels in lines:
        if is_increasing_or_decreasing(levels) and is_gradual(levels):
            safe += 1
        else:
            for i in range(1, len(levels) + 1):
                dampened = levels[: i - 1] + levels[i:]
                if is_increasing_or_decreasing(dampened) and is_gradual(dampened):
                    safe_damp += 1
                    break

    print(f"Part 1: {safe}")
    print(f"Part 2: {safe + safe_damp}")


if __name__ == "__main__":
    main()
