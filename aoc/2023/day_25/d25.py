from aoc.cli import file_input
from aoc.data_structures import PriorityQueue
from itertools import combinations
from collections import defaultdict
import graphviz


def dj(graph: dict[str, set[str]], start: str, end: str) -> list[str]:
    dist = {}
    prev = {}
    dist[start] = 0
    pq = PriorityQueue(pq_removed_item="1234")
    pq.add(start, 0)

    while pq:
        v = pq.pop()
        for n in graph[v]:
            d = dist.get(v) + 1
            if d < dist.get(n, 9999999999999):
                dist[n] = d
                prev[n] = v
                pq.add(n, d)
    path = [end]
    while path[-1] != start:
        path.append(prev[path[-1]])
    return list(reversed(path))


def main() -> None:
    g = graphviz.Graph("G", filename="process.gv", engine="sfdp")

    cut = {("dct", "kns"), ("nqq", "pxp"), ("jxb", "ksq")}
    wires = {}
    wire_names = set()
    with file_input() as file:
        while line := file.readline().strip():
            l, neighbors = line.split(": ")
            wire_names.add(l)
            if l not in wires:
                wires[l] = set()
            neighbors = neighbors.split()
            for n in neighbors:
                if n not in wires:
                    wires[n] = set()

                if tuple(sorted([n, l])) not in cut:
                    g.edge(l, n)
                    g.edge(n, l)
                    wire_names.add(n)
                    wires[l].add(n)
                    wires[n].add(l)

    g.view()

    left = set()
    left.add("dct")
    right = set()
    right.add("kns")
    while len(left | right) < len(wire_names):
        for name in wire_names:
            if name in left:
                left |= wires[name]
            elif name in right:
                right |= wires[name]
            elif wires[name] & left:
                left.add(name)
                left |= wires[name]
            elif wires[name] & right:
                right.add(name)
                right |= wires[name]

    print(f"Part 1: {len(left)} * {len(right)} = {len(left) * len(right)}")


if __name__ == "__main__":
    main()
