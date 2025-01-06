from aoc.cli import file_input
from aoc.geometry import Point, CARDINAL_DIRECTIONS, in_bounds, up, down, right, left
from aoc.print_tools import Color


CANT_TRAVEL = {
    ">": left,
    "<": right,
    "^": up,
    "v": down,
    ".": None,
}


def make_better_graph(graph: list[str], start: Point, end: Point) -> dict[Point, set[Point]]:
    stack = [start]
    better_graph = {}

    while stack:
        p = stack.pop()
        if p in better_graph:
            continue
        better_graph[p] = set()
        for d in CARDINAL_DIRECTIONS:
            n = d(p)
            if not in_bounds(n, len(graph[0]), len(graph)) or graph[n.y][n.x] == "#":
                continue
            better_graph[p].add(n)
            stack.append(n)

    return better_graph


def compress_graph(graph: dict[Point, set[Point]], start: Point) -> dict[Point, dict[Point, int]]:
    stack = [start]
    compressed_graph = {}

    while stack:
        p = stack.pop()
        if p in compressed_graph:
            continue
        compressed_graph[p] = {}

        paths = []
        for n in graph[p]:
            paths.append([p, n])
        ended_paths = []
        while paths:
            path = paths.pop()
            end = path[-1]
            neighbors = graph[end]
            if len(neighbors) != 2:
                ended_paths.append(path)
                continue
            path_set = set(path)
            for n in neighbors:
                if n not in path_set:
                    path.append(n)
            paths.append(path)

        for path in ended_paths:
            compressed_graph[p][path[-1]] = len(path) - 1
            stack.append(path[-1])

    return compressed_graph


def dfs_compressed_graph(graph: dict[Point, dict[Point, int]], start: Point, end: Point) -> int:
    stack = [[start]]
    max_path = 0
    while stack:
        path = stack.pop()

        path_end = path[-1]
        if path_end == end:
            p = path[0]
            d = 0
            for np in path[1:]:
                d += graph[p][np]
                p = np
            if d > max_path:
                # print(f"LONGER PATH! -> {d} -> {path}")
                max_path = d
            continue

        path_set = set(path)
        for neighbor in graph[path_end]:
            if neighbor in path_set:
                continue
            new_path = path.copy()
            new_path.append(neighbor)
            stack.append(new_path)

    return max_path


def p1(graph: list[str], start: Point, end: Point) -> int:
    stack = [[start]]
    max_path = 0
    while stack:
        path = stack.pop()

        if path[-1] == end:
            max_path = max(max_path, len(path)-1)
            continue

        for d in CARDINAL_DIRECTIONS:
            n = d(path[-1])

            sub_path = [n]
            path_set = set(path)

            if n in path_set or not in_bounds(n, len(graph[0]), len(graph)) or graph[n.y][n.x] == "#":
                continue

            tile = graph[n.y][n.x]
            if d == CANT_TRAVEL[tile]:
                continue

            while graph[n.y][n.x] in {">", "<", "v", "^"}:
                n = d(n)
                sub_path.append(n)

            if path_set & set(sub_path):
                continue

            new_path = path.copy()
            new_path.extend(sub_path)
            stack.append(new_path)

    return max_path


def main() -> None:
    graph = []
    with file_input() as file:
        while line := file.readline().strip():
            graph.append(line)
            print(line)

    for x in range(len(graph[0])):
        if graph[0][x] == ".":
            start = Point(x, 0)
            break
    for x in reversed(range(len(graph[-1]))):
        if graph[-1][x] == ".":
            end = Point(x, len(graph) - 1)
            break
    better_graph = make_better_graph(graph, start, end)
    for k, v in better_graph.items():
        print(f"{k} -> {v}")
    print()
    compressed_graph = compress_graph(better_graph, start)
    for k, v in compressed_graph.items():
        print(f"{k} -> {v}")
    print(f"{start=}, {end=}")

    for y, row in enumerate(graph):
        row_str = ""
        for x in range(len(row)):
            p = Point(x, y)
            if p in compressed_graph:
                row_str += Color.GREEN + graph[y][x] + Color.END
            else:
                row_str += graph[y][x]
        print(row_str)

    print(f"Part 1: {p1(graph, start, end)}")
    print(f"Part 2: {dfs_compressed_graph(compressed_graph, start, end)}")


if __name__ == "__main__":
    main()
