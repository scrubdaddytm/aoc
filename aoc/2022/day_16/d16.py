from aoc.cli import file_input
from collections import deque
from itertools import combinations
from itertools import chain
import re


def shortest_path(source, target, graph) -> tuple[int, dict]:
    seen = set()
    path = {}
    q = deque()
    q.append((source, 0))

    while q:
        v, d = q.popleft()
        seen.add(v)
        for n_v in graph[v][1]:
            if not n_v in seen:
                path[n_v] = v
                q.append((n_v, d + 1))
            if n_v == target:
                return d + 1, path

    return len(graph.keys()), path


def calculate_distance_and_path_matrices(graph):
    distance_matrix = {s: {} for s in graph.keys()}
    for s in graph:
        for t in graph:
            if s == t:
                continue
            distance_matrix[s][t], path = shortest_path(s, t, graph)
    return distance_matrix


def traverse(source: str, graph: dict[str, tuple[int, list[str]]], valves_to_open: set | None = None, rounds: int = 30) -> int:
    distance_matrix = calculate_distance_and_path_matrices(graph)

    non_zero_valves = set()
    if valves_to_open:
        non_zero_valves = valves_to_open
    else:
        for v, vals in graph.items():
            if vals[0] > 0:
                non_zero_valves.add(v)

    open_valves = set()

    def backtrack(s, flow, count):
        if count >= rounds or open_valves == non_zero_valves:
            return flow
        flows = []
        for v in non_zero_valves - open_valves:
            dist = distance_matrix[s][v]
            if count + dist + 1 > rounds:
                continue
            open_valves.add(v)
            new_flow = (rounds - (count + dist + 1)) * graph[v][0]
            flows.append(backtrack(v, flow + new_flow, count + dist + 1))
            open_valves.remove(v)
        return max(flows) if flows else flow

    return backtrack(source, 0, 0)


def main() -> None:
    valves = {}
    with file_input() as file:
        p = re.compile(r"Valve (\w+) has flow rate=(-?\d+); tunnels? leads? to valves? (.*)")
        while line := file.readline():
            result = p.match(line)
            valves[result.group(1)] = (int(result.group(2)), result.group(3).split(", "))

    max_flow = traverse("AA", valves)
    print(f"{max_flow}")

    non_zero_valves = set()
    for v, vals in valves.items():
        if vals[0] > 0:
            non_zero_valves.add(v)

    max_flow_with_ele = 0
    len_nonz = len(non_zero_valves)
    for subset in chain.from_iterable(combinations(non_zero_valves, r) for r in range((len_nonz // 2) + 1, (len_nonz // 2) + 2)):
        my_valves = set(subset)
        ele_valves = non_zero_valves - my_valves
        flow = traverse("AA", valves, my_valves, 26) + traverse("AA", valves, ele_valves, 26)
        if flow > max_flow_with_ele:
            print(f"checked: {my_valves} and {ele_valves}")
            print(f"~~~ new max: {flow} ~~~~")
            max_flow_with_ele = flow
    print(f"{max_flow_with_ele=}")


if __name__ == "__main__":
    main()
