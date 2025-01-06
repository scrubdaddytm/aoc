from aoc.cli import file_input
from aoc.geometry import CARDINAL_DIRECTIONS, in_bounds, Point


def p1(graph: tuple[str], start: Point, steps: int) -> dict[Point, int]:
    points = set([start])
    for step in range(1, steps + 1):
        next_points = set()
        for p in points:
            for d in CARDINAL_DIRECTIONS:
                next_p = d(p)
                if not in_bounds(next_p, len(graph[0]), len(graph)) or graph[next_p.y][next_p.x] == "#":
                    continue
                next_points.add(next_p)
        points = next_points
    return len(points)


def find_distances(graph: tuple[str], start: Point, steps: int) -> dict[Point, int]:
    distances = {}
    points = set([start])
    for step in range(1, steps + 1):
        next_points = set()
        for p in points:
            for d in CARDINAL_DIRECTIONS:
                next_p = d(p)
                if distances.get(next_p) or graph[next_p.y % 131][next_p.x % 131] == "#":
                    continue
                distances[next_p] = step
                next_points.add(next_p)
        points = next_points
    print(len(distances.values()))
    return len(list(filter(lambda d: (d % 2) == (steps % 2), distances.values())))


def main() -> None:
    graph = []
    start = None
    with file_input() as file:
        y = 0
        while line := file.readline().strip():
            graph.append(line)
            if (x := line.find("S")) != -1:
                start = Point(x, y)
            y += 1
    graph = tuple(graph)
    print(f"{start=}, in {len(graph[0])}x{len(graph)}")

    p1_count = p1(graph, start, 64)
    print(f"Part 1: {p1_count}")

    # Quad Fit
    n = 26501365
    x_0 = n % len(graph)
    x_1 = x_0 + len(graph)
    x_2 = x_0 + (2 * len(graph))

    fx_0 = find_distances(graph, start, x_0)
    fx_1 = find_distances(graph, start, x_1)
    fx_2 = find_distances(graph, start, x_2)

    print(f"{x_0=}, {x_1=}, {x_2=}")
    print(f"{fx_0=}, {fx_1=}, {fx_2=}")

    p2_quad_fit = 0

    b0 = fx_0
    b1 = fx_1 - fx_0
    b2 = fx_2 - fx_1
    p2_quad_fit += b0
    p2_quad_fit += b1 * x
    p2_quad_fit += (x * (x - 1) // 2) * (b2 - b1)

    print(f"Part 2: {p2_quad_fit}")


if __name__ == "__main__":
    main()
