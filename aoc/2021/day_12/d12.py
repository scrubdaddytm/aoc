from aoc.cli import file_input
from collections import defaultdict


def dfs(
    stack: list[str],
    graph: dict[str, set[str]],
    smol_caves: set[str],
    total_smol_caves: int,
) -> int:
    if not stack:
        return 0

    vertex = stack[-1]
    if vertex == "end":
        print(f"{','.join(stack)}")
        return 1

    paths = 0

    for edge in graph[vertex]:
        # print(f"{vertex} -> {edge}")
        if edge in smol_caves:
            continue
        elif edge.islower():
            smol_caves.add(edge)
        stack.append(edge)

        paths += dfs(stack, graph, smol_caves, total_smol_caves)

        stack.pop()
        smol_caves.discard(edge)

    return paths


def main() -> None:
    graph = defaultdict(set)
    smol_caves = set()
    with file_input() as file:
        while line := file.readline().strip():
            vertices = line.split("-")
            graph[vertices[0]].add(vertices[1])
            graph[vertices[1]].add(vertices[0])
            for vertex in vertices:
                if vertex.islower():
                    smol_caves.add(vertex)

    print(f"{graph=}")
    print(f"{smol_caves=}")

    paths = dfs(["start"], graph, {"start"}, len(smol_caves)-1)
    print(f"part 1: {paths=}")


if __name__ == "__main__":
    main()
