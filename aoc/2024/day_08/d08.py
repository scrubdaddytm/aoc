from aoc.cli import file_input
from dataclasses import dataclass
from collections import defaultdict
from aoc.geometry import Point
from aoc.print_tools import print_grid
from aoc.geometry import in_bounds
from functools import partial
from itertools import combinations


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
        print_grid, min_x=0, min_y=0, max_x=max_j - 1, max_y=max_i - 1
    )
    in_b = partial(in_bounds, min_x=0, min_y=0, max_x=max_j, max_y=max_i)

    print_graph(graph)

    antinodes_p1 = set()
    antinodes_p2 = set()
    for c, points in node_lines.items():
        print(f"{c=}")
        for a, b in combinations(points, 2):
            a, b = sorted([a, b])

            a_delta = Point(-(b.x - a.x), -(b.y - a.y))
            b_delta = Point((b.x - a.x), (b.y - a.y))

            anode_a = a.move(a_delta)
            anode_b = b.move(b_delta)
            if in_b(anode_a):
                antinodes_p1.add(anode_a)
                while in_b(anode_a):
                    antinodes_p2.add(anode_a)
                    anode_a = anode_a.move(a_delta)

            if in_b(anode_b):
                antinodes_p1.add(anode_b)
                while in_b(anode_b):
                    antinodes_p2.add(anode_b)
                    anode_b = anode_b.move(b_delta)

    anode_graph_p1 = {a: "#" for a in antinodes_p1}
    anode_graph_p2 = {a: "#" for a in antinodes_p2}
    print_graph(anode_graph_p1 | graph)
    print_graph(anode_graph_p2 | graph)

    print(f"Part 1: {len(antinodes_p1)}")
    print(f"Part 2: {len(antinodes_p2 | {p for p in graph})}")


if __name__ == "__main__":
    main()
