from aoc.cli import file_input
from aoc.geometry import Point, in_bounds, CARDINAL_DIRECTIONS
from aoc.data_structures import PriorityQueue


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
    pq = PriorityQueue(pq_removed_item=Point(-1, -1))
    DEFAULT_DISTANCE = 999999999

    for y in range(end.y + 1):
        for x in range(end.x + 1):
            point = Point(x, y)
            distance[point] = DEFAULT_DISTANCE
            prev[point] = None
            pq.add(Point(x, y), DEFAULT_DISTANCE)

    distance[start] = 0
    pq.remove(start)
    pq.add(start, distance[start])

    while pq:
        vertex = pq.pop()
        for direction in CARDINAL_DIRECTIONS:
            next_vertex = direction(vertex)
            if in_bounds(next_vertex, max_x=end.x + 1, max_y=end.y + 1):
                alt_dist = distance[vertex] + point_graph[next_vertex]
                if alt_dist < distance[next_vertex]:
                    distance[next_vertex] = alt_dist
                    prev[next_vertex] = vertex
                    pq.remove(next_vertex)
                    pq.add(next_vertex, alt_dist)

    print(f"part 1: {distance[p1_end]}")
    print(f"part 2: {distance[end]}")


if __name__ == "__main__":
    main()
