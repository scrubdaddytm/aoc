from collections import defaultdict
from itertools import combinations

from aoc.cli import file_input


def main() -> None:
    network = defaultdict(set)
    with file_input() as file:
        while line := file.readline().strip():
            a, b = line.split("-")
            network[a].add(b)
            network[b].add(a)

    p1 = 0

    three_sets = set()
    for comp in network:
        for a, b in combinations(network[comp], 2):
            if a in network[b]:
                three_sets.add(frozenset([comp, a, b]))

    for s in three_sets:
        for comp in s:
            if comp[0] == "t":
                p1 += 1
                break

    deeper = three_sets
    while len(deeper) > 1:
        onemore = set()
        for t in deeper:
            comps = list(t)
            for maybe_connected in network[comps[0]]:
                if maybe_connected in t:
                    continue
                if all([maybe_connected in network[c] for c in comps]):
                    onemore.add(frozenset(comps + [maybe_connected]))
        deeper = onemore
    biggest = list(deeper)[0]

    print(f"Part 1: {p1}")
    print(f"Part 2: {','.join(sorted(biggest))}")


if __name__ == "__main__":
    main()
