from aoc.cli import file_input
from collections import defaultdict


def dfs(
    stack: list[str],
    graph: dict[str, list[str]],
    smol_caves: set[str],
    doubled_up: str = "",
) -> int:
    if not stack:
        return 0

    vertex = stack[-1]
    if vertex == "end":
        print(f"{','.join(stack)}")
        return 1

    paths = 0

    old_double = doubled_up
    for edge in graph[vertex]:
        if edge == "start" or (edge in smol_caves and doubled_up != ""):
            continue
        elif edge in smol_caves:
            doubled_up = edge
        elif edge.islower():
            smol_caves.add(edge)
        stack.append(edge)

        paths += dfs(stack, graph, smol_caves, doubled_up)

        stack.pop()
        if old_double == doubled_up:
            smol_caves.discard(edge)
        else:
            doubled_up = old_double

    return paths


def main() -> None:
    graph = defaultdict(list)
    smol_caves = set()
    with file_input() as file:
        while line := file.readline().strip():
            vertices = line.split("-")
            if vertices[1] not in graph[vertices[0]]:
                graph[vertices[0]].append(vertices[1])
            if vertices[0] not in graph[vertices[1]]:
                graph[vertices[1]].append(vertices[0])
            for vertex in vertices:
                if vertex.islower():
                    smol_caves.add(vertex)

    for edge in graph.keys():
        graph[edge] = sorted(graph[edge])

    print(f"{graph=}")
    print(f"{smol_caves=}")

    paths = dfs(["start"], graph, {"start"}, "start")
    print(f"\npart 1: {paths=}\n")

    paths = dfs(["start"], graph, {"start"})
    print(f"\npart 2: {paths=}\n")


if __name__ == "__main__":
    main()
