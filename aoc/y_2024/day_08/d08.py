from collections import defaultdict
from functools import partial
from itertools import combinations

from aoc.cli import file_input
from aoc.geometry import Point, in_bounds
from aoc.print_tools import print_grid


def find_anodes(
    point: Point,
    p_delta: Point,
    in_b: callable,
    limit: bool = False,
) -> set[Point]:
    antinodes = set()
    while in_b(point):
        antinodes.add(point)
        if limit:
            break
        point = point.move(p_delta)
    return antinodes


def main() -> None:
    graph = {}
    node_lines = defaultdict(list)
    max_j = 0
    with file_input() as file:
        i = 0
        while line := file.readline().strip():
            for j, c in enumerate(line):
                if c != ".":
                    p = Point(j, i)
                    graph[p] = c
                    node_lines[c].append(p)
            i += 1
            max_j = len(line)

    max_i = i
    print_graph = partial(
        print_grid,
        min_x=0,
        min_y=0,
        max_x=max_j - 1,
        max_y=max_i - 1,
    )
    in_b = partial(
        in_bounds,
        min_x=0,
        min_y=0,
        max_x=max_j,
        max_y=max_i,
    )

    print_graph(graph)

    antinodes_p1 = set()
    antinodes_p2 = set()
    for c, points in node_lines.items():
        for a, b in combinations(points, 2):
            a_delta = Point(-(b.x - a.x), -(b.y - a.y))
            anode_a = a.move(a_delta)
            antinodes_p1 |= find_anodes(anode_a, a_delta, in_b, limit=True)
            antinodes_p2 |= find_anodes(anode_a, a_delta, in_b)

            b_delta = Point((b.x - a.x), (b.y - a.y))
            anode_b = b.move(b_delta)
            antinodes_p1 |= find_anodes(anode_b, b_delta, in_b, limit=True)
            antinodes_p2 |= find_anodes(anode_b, b_delta, in_b)

    print_graph({a: "#" for a in antinodes_p1} | graph)
    print_graph({a: "#" for a in antinodes_p2} | graph)

    print(f"Part 1: {len(antinodes_p1)}")
    print(f"Part 2: {len(antinodes_p2 | {p for p in graph})}")


if __name__ == "__main__":
    main()
