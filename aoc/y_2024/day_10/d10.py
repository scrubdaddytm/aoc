from collections import defaultdict, deque

from aoc.cli import file_input
from aoc.geometry import CARDINAL_DIRECTIONS, Point


def find_trails(
    topo_map: dict[Point, int],
    trailheads: set[Point],
) -> dict[Point, set[Point]]:
    access = defaultdict(set)

    for trailhead in trailheads:
        seen = set()
        q = deque()
        q.append(trailhead)

        while q:
            p = q.popleft()
            if p in seen:
                continue
            seen.add(p)
            p_val = topo_map[p]

            for d in CARDINAL_DIRECTIONS:
                next_cell = d(p)
                if next_cell not in topo_map:
                    continue

                next_val = topo_map[next_cell]
                if next_val == p_val + 1:
                    if next_val == 9:
                        access[trailhead].add(next_cell)
                    if next_cell not in seen:
                        q.append(next_cell)

    return access


def distinct_trails(
    topo_map: dict[Point, int],
    ends: set[Point],
) -> dict[Point, int]:
    access = defaultdict(int)

    seen = set()
    q = deque()
    for end in ends:
        q.append(end)
        access[end] = 1

    while q:
        p = q.popleft()
        if p in seen:
            continue
        seen.add(p)
        p_val = topo_map[p]

        for d in CARDINAL_DIRECTIONS:
            next_cell = d(p)
            if next_cell not in topo_map:
                continue

            next_val = topo_map[next_cell]
            if next_val == p_val - 1:
                access[next_cell] += access[p]
                if next_cell not in seen:
                    q.append(next_cell)

    return access


def main() -> None:
    topo_map = {}
    trailheads = set()
    ends = set()
    with file_input() as file:
        i = 0
        while line := file.readline().strip():
            for j, c in enumerate(line):
                if c == ".":
                    continue
                c_int = int(c)
                p = Point(j, i)
                topo_map[p] = c_int
                if c_int == 0:
                    trailheads.add(p)
                elif c_int == 9:
                    ends.add(p)
            i += 1

    p1_access = find_trails(topo_map, trailheads)
    p2_access = distinct_trails(topo_map, ends)
    p1 = sum(len(p1_access[trailhead]) for trailhead in trailheads)
    p2 = sum(p2_access[trailhead] for trailhead in trailheads)

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
