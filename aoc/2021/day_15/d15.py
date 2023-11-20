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
    end = Point(len(graph[0]) - 1, len(graph) - 1)

    print(f"{start=}, {end=}")

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
                alt_dist = distance[vertex] + graph[next_vertex.y][next_vertex.x]
                if alt_dist < distance[next_vertex]:
                    distance[next_vertex] = alt_dist
                    prev[next_vertex] = vertex
                    remove_from_pq(pq, next_vertex)
                    add_to_pq(pq, next_vertex, alt_dist)

    print(f"part 1: {distance[end]}")


if __name__ == "__main__":
    main()
