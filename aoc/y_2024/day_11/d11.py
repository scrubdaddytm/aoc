from collections import Counter
from functools import cache

from aoc.cli import file_input


@cache
def change(stone: int) -> tuple[int]:
    if stone == 0:
        return (1,)
    stone_str = str(stone)
    stone_digits = len(stone_str)
    if stone_digits % 2 == 0:
        return (
            int(stone_str[: stone_digits // 2]),
            int(stone_str[stone_digits // 2:]),
        )
    else:
        return (stone * 2024,)


def run_blinks(stones: tuple[int], limit: int = 25) -> tuple[int]:
    counts = Counter(stones)

    for b in range(limit):
        new_count = Counter()
        for stone, count in counts.items():
            changed = change(stone)
            for new_stone in changed:
                new_count[new_stone] += count
        counts = new_count

    return sum(v for v in counts.values())


def main() -> None:
    stones = []
    with file_input() as file:
        while line := file.readline().strip():
            stones = tuple(map(int, line.split()))

    p1 = run_blinks(stones, limit=25)
    print(f"Part 1: {p1}")

    p2 = run_blinks(stones, limit=75)
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
