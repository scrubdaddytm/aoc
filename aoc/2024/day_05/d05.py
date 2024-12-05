from aoc.cli import file_input
from dataclasses import dataclass
from collections import defaultdict
from functools import cmp_to_key


def is_ordered(update: list[int], pages: dict[int, set[int]]) -> bool:
    seen = set()
    for page in update:
        seen.add(page)
        # print(f"{page}: {pages[page]} & {seen} == {pages[page] & seen}")
        if pages[page] & seen:
            return False

    return True


def main() -> None:
    pages = defaultdict(set)
    updates = []
    with file_input() as file:
        while line := file.readline().strip():
            x, y = map(int, line.split("|"))
            pages[x].add(y)
        while line := file.readline().strip():
            updates.append(list(map(int, line.split(","))))

    p1 = 0
    p2 = 0

    for update in updates:
        if is_ordered(update, pages):
            p1 += update[len(update) // 2]

        else:
            sorted_update = sorted(
                update, key=cmp_to_key(lambda x, y: -1 if y in pages[x] else abs(x - y))
            )
            p2 += sorted_update[len(sorted_update) // 2]

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
