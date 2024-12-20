import sys
from collections import defaultdict

from aoc.cli import file_input
from aoc.data_structures import PriorityQueue
from aoc.geometry import CARDINAL_DIRECTIONS, Point


def solve_maze(
    end: Point,
    maze: set[Point],
) -> tuple[dict[Point, Point], dict[Point, int]]:
    q = PriorityQueue(pq_removed_item=Point(-1, -1))
    dist = {}
    prev = {}
    dist[end] = 0
    for p in maze:
        q.add(p, sys.maxsize)
    q.add(end, 0)

    while q:
        p = q.pop()
        curr_dist = dist[p]

        for d in CARDINAL_DIRECTIONS:
            new_p = d(p)
            if new_p in maze and (new_p not in dist or dist[new_p] > curr_dist + 1):
                dist[new_p] = curr_dist + 1
                prev[new_p] = p
                q.add(new_p, curr_dist + 1)

    return prev, dist


def find_cheat_points(p: Point, maze: set[Point], time: int = 2) -> set[Point]:
    cheat_points = set()
    for dy in range(-time, time + 1):
        for dx in range(-time, time + 1):
            if (dx == 0 and dy == 0) or abs(dx) + abs(dy) > time:
                continue
            cheat_points.add(Point(p.x + dx, p.y + dy))
    return cheat_points & maze


def cheat(
    start: Point,
    end: Point,
    maze: set[Point],
    dist: dict[Point, int],
    prev: dict[Point, Point],
    cheat_time: int = 2,
) -> dict[int, int]:
    saved = defaultdict(int)
    no_cheat_dist = dist[start]
    p = start
    while p != end:
        curr_dist = no_cheat_dist - dist[p]
        for cheat_p in find_cheat_points(p, maze, cheat_time):
            cheat_dist = curr_dist + p.distance(cheat_p) + dist[cheat_p]
            if no_cheat_dist - cheat_dist > 0:
                saved[no_cheat_dist - cheat_dist] += 1
        p = prev[p]
    return saved


def main() -> None:
    maze = set()
    start = end = None
    y = x = 0
    with file_input() as file:
        while line := file.readline().strip():
            for x, c in enumerate(line):
                if c == "#":
                    continue
                p = Point(x, y)
                maze.add(p)
                if c == "S":
                    start = p
                elif c == "E":
                    end = p
            y += 1
    prev, dist = solve_maze(end, maze)

    saved_p1 = cheat(start, end, maze, dist, prev)
    saved_p2 = cheat(start, end, maze, dist, prev, 20)

    p1 = 0
    p2 = 0

    for save, count in saved_p1.items():
        if save >= 100:
            p1 += count

    for save, count in saved_p2.items():
        if save >= 100:
            p2 += count

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
