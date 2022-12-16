from aoc.cli import file_input
from collections import deque
from itertools import combinations
import re


def shortest_path_len(source, target, graph) -> int:
    seen = set()
    q = deque()
    q.append((source, 0))

    while q:
        v, d = q.popleft()
        seen.add(v)
        for n_v in graph[v][1]:
            if n_v == target:
                return d + 1
            if not n_v in seen:
                q.append((n_v, d + 1))

    return len(graph.keys())


def calculate_distance_matrix(graph):
    distance_matrix = {s: {} for s in graph.keys()}
    for s in graph:
        for t in graph:
            if s == t:
                continue
            distance_matrix[s][t] = shortest_path_len(s, t, graph)
        print(f"{s} -> {distance_matrix[s].items()}")
    return distance_matrix
        

def traverse_with_elephant(source: str, graph: dict[str, tuple[int, list[str]]]) -> int:
    # THIS IS WRONG :(
    distance_matrix = calculate_distance_matrix(graph)
    non_zero_valves = set()
    for v, vals in graph.items():
        if vals[0] > 0:
            non_zero_valves.add(v)
    open_valves = set()

    def backtrack(me, me_wait, ele, ele_wait, flow, count):
        if count >= 26 or open_valves == non_zero_valves:
            return flow
        print(f"round {count}: {me=}, waiting={me_wait} ~ {ele=}, waiting={ele_wait} - {flow}")
        flows = []
        if me_wait == 0 and ele_wait == 0:
            if count > 0:
                flow += ((26 - count) * graph[me][0]) + ((26 - count) * graph[ele][0])

            for combo in combinations(non_zero_valves - open_valves, 2):
                dist_me = distance_matrix[me][combo[0]]
                dist_ele = distance_matrix[ele][combo[1]]
                open_valves.add(combo[0])
                open_valves.add(combo[1])
                flows.append(backtrack(combo[0], dist_me, combo[1], dist_ele, flow, count+1))
                open_valves.remove(combo[0])
                open_valves.remove(combo[1])

        elif me_wait == 0:
            flow += (26 - count) * graph[me][0]
            for next_me in (non_zero_valves - open_valves):
                open_valves.add(next_me)
                dist_me = distance_matrix[me][next_me]
                flows.append(backtrack(next_me, dist_me, ele, ele_wait-1, flow, count+1))
                open_valves.remove(next_me)

        elif ele_wait == 0:
            flow += (26 - count) * graph[ele][0]
            for next_ele in (non_zero_valves - open_valves):
                open_valves.add(next_ele)
                dist_ele = distance_matrix[ele][next_ele]
                flows.append(backtrack(me, me_wait-1, next_ele, dist_ele, flow, count+1))
                open_valves.remove(next_ele)

        else:
            flows.append(backtrack(me, me_wait-1, ele, ele_wait-1, flow, count+1))

        return max(flows) if flows else 0
    return backtrack(source, 0, source, 0, 0, 0)

def traverse(source: str, graph: dict[str, tuple[int, list[str]]]) -> int:
    distance_matrix = calculate_distance_matrix(graph)

    non_zero_valves = set()
    for v, vals in graph.items():
        if vals[0] > 0:
            non_zero_valves.add(v)

    open_valves = set()

    def backtrack(s, flow, count):
        if count >= 30 or open_valves == non_zero_valves:
            return flow
        flows = []
        for v in (non_zero_valves - open_valves):
            open_valves.add(v)
            dist = distance_matrix[s][v]
            new_flow = (30 - (count+dist+1)) * graph[v][0]
            flows.append(backtrack(v, flow+new_flow, count+dist+1))
            open_valves.remove(v)
        return max(flows)
    return backtrack(source, 0, 0)


def main() -> None:
    valves = {}
    with file_input() as file:
        p = re.compile(r"Valve (\w+) has flow rate=(-?\d+); tunnels? leads? to valves? (.*)")
        while line := file.readline():
            result = p.match(line)
            valves[result.group(1)] = (int(result.group(2)), result.group(3).split(', '))

    max_flow = traverse("AA",  valves)
    print(f"{max_flow}")

    max_flow_with_elephant = traverse_with_elephant("AA", valves)
    print(f"{max_flow_with_elephant}")

if __name__ == "__main__":
    main()