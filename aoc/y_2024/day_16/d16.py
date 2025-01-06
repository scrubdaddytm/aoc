import sys
from collections import deque

from aoc.cli import file_input
from aoc.data_structures import PriorityQueue
from aoc.geometry import (CLOCKWISE, COUNTER_CLOCKWISE, Point, down, left,
                          right, up)
from aoc.print_tools import Color, print_grid

right, up

PRINT_DIRECTION = {
    up: "v",
    left: "<",
    down: "^",
    right: ">",
}
STR_DIRECTION = {
    "v": up,
    "<": left,
    "^": down,
    ">": right,
}


def print_maze(graph: set[Point], path: set[Point, callable], end: Point) -> None:
    printable_graph = {p: "." for p in graph}
    for p, direction in path:
        printable_graph[p] = Color.CYAN + \
            PRINT_DIRECTION[direction] + Color.END
    printable_graph[end] = Color.RED + "E" + Color.END
    print_grid(printable_graph, default_str="#")


def get_path_points(
    end: tuple[Point, str],
    prev: dict[tuple[Point, str], set[tuple[Point, str]]],
) -> set[Point]:
    path_points = set()
    path_points.add(end[0])
    q = deque()
    q.append(end)
    while q:
        pos = q.popleft()
        if pos in prev:
            for next_pos in prev[pos]:
                p, _ = next_pos
                path_points.add(p)
                q.append(next_pos)
    return path_points


def shortest_path(graph: set[Point], start: Point, end: Point) -> tuple[int, int]:
    dist = {(start, ">"): 0}
    prev = {}
    q = PriorityQueue(pq_removed_item=(Point(9999, 9999), "SENTINEL"))
    q.add((start, ">"), 0)

    while q:
        curr_state = q.pop()
        pos, d = curr_state
        direction = STR_DIRECTION[d]
        curr_dist = dist[curr_state]

        next_cell = direction(pos)
        alt_dist_moved = 1 + curr_dist
        new_state = (next_cell, d)
        if next_cell in graph:
            if new_state not in dist or alt_dist_moved < dist[new_state]:
                dist[new_state] = alt_dist_moved
                q.add(new_state, alt_dist_moved)
                prev[new_state] = {curr_state}
            elif alt_dist_moved == dist[new_state]:
                prev[new_state].add(curr_state)

        for new_d in (CLOCKWISE[direction], COUNTER_CLOCKWISE[direction]):
            alt_dist = 1000 + curr_dist
            new_state = (pos, PRINT_DIRECTION[new_d])
            if new_state not in dist or alt_dist < dist[new_state]:
                dist[new_state] = alt_dist
                prev[new_state] = {curr_state}
                q.add(new_state, alt_dist)
            elif alt_dist == dist[new_state]:
                prev[new_state].add(curr_state)

    min_d = sys.maxsize
    path = None
    for c in STR_DIRECTION.keys():
        d = dist.get((end, c), -1)
        print(f"{c} -> {d}")
        if d > 0:
            if d < min_d:
                min_d = min(min_d, d)
                path = get_path_points((end, c), prev)
    return min_d, len(path)


def main() -> None:
    graph = set()
    start = None
    end = None
    with file_input() as file:
        y = 0
        while line := file.readline().strip():
            for x, c in enumerate(line):
                if c == ".":
                    graph.add(Point(x, y))
                elif c == "S":
                    start = Point(x, y)
                    graph.add(start)
                elif c == "E":
                    end = Point(x, y)
                    graph.add(end)
            y += 1

    print_maze(graph, {(start, right)}, end)

    p1, p2 = shortest_path(graph, start, end)

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
