from aoc.cli import file_input
from aoc.geometry import Point, in_bounds, CARDINAL_DIRECTIONS
import heapq


PQ_REMOVED = Point(-1, -1)
entry_finder = {}


def add_to_pq(pq: list[tuple[int, Point]], point: Point, prio: int) -> None:
    if point in entry_finder:
        remove_from_pq(point)
    entry = [prio, point]
    entry_finder[point] = entry
    heapq.heappush(pq, entry)


def remove_from_pq(pq: list[tuple[int, Point]], point: Point) -> None:
    entry = entry_finder.pop(point)
    entry[-1] = PQ_REMOVED


def pop_from_pq(pq: list[tuple[int, Point]]) -> Point:
    while pq:
        prio, point = heapq.heappop(pq)
        if point is not PQ_REMOVED:
            del entry_finder[point]
            return point
    raise KeyError("pop from empty pq")


def main() -> None:
    graph = []
    with file_input() as file:
        while line := file.readline().strip():
            graph.append(list(map(int, list(line))))

    start = Point(0, 0)
    tile_x = len(graph[0])
    tile_y = len(graph)
    p1_end = Point(tile_x - 1, tile_y - 1)
    end = Point((tile_x * 5) - 1, ((tile_y) * 5) - 1)

    print(f"{tile_x=}, {tile_y=}, {p1_end=}, {end=}")

    point_graph = {}

    for y in range(tile_y * 5):
        for x in range(tile_x * 5):
            point = Point(x, y)
            dist = 9999999999
            if x < tile_x and y < tile_y:
                dist = graph[y][x]
            else:
                up = Point(x, y - tile_y)
                left = Point(x - tile_x, y)
                if in_bounds(up, tile_x * 5, tile_y * 5):
                    dist = point_graph[up] + 1
                else:
                    dist = point_graph[left] + 1
            if dist > 9:
                dist = 1
            point_graph[point] = dist

    distance = {}
    prev = {}
    pq = []
    DEFAULT_DISTANCE = 999999999

    for y in range(end.y + 1):
        for x in range(end.x + 1):
            point = Point(x, y)
            distance[point] = DEFAULT_DISTANCE
            prev[point] = None
            add_to_pq(pq, Point(x, y), DEFAULT_DISTANCE)

    distance[start] = 0
    remove_from_pq(pq, start)
    add_to_pq(pq, start, distance[start])

    while pq:
        try:
            vertex = pop_from_pq(pq)
        except KeyError:
            pass
        for direction in CARDINAL_DIRECTIONS:
            next_vertex = direction(vertex)
            if in_bounds(next_vertex, max_x=end.x + 1, max_y=end.y + 1):
                alt_dist = distance[vertex] + point_graph[next_vertex]
                if alt_dist < distance[next_vertex]:
                    distance[next_vertex] = alt_dist
                    prev[next_vertex] = vertex
                    remove_from_pq(pq, next_vertex)
                    add_to_pq(pq, next_vertex, alt_dist)

    print(f"part 1: {distance[p1_end]}")
    print(f"part 2: {distance[end]}")


if __name__ == "__main__":
    main()
