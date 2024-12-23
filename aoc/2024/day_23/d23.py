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
        if any(comp[0] == "t" for comp in s):
            p1 += 1

    deeper = three_sets
    while len(deeper) > 1:
        onemore = set()
        for comps in deeper:
            for maybe_connected in filter(
                lambda m: m not in comps, network[list(comps)[0]]
            ):
                if all([maybe_connected in network[c] for c in comps]):
                    onemore.add(frozenset(comps | set([maybe_connected])))
        deeper = onemore
    biggest = list(deeper)[0]

    print(f"Part 1: {p1}")
    print(f"Part 2: {','.join(sorted(biggest))}")


if __name__ == "__main__":
    main()
