from dataclasses import dataclass
from aoc.cli import file_input
import heapq


@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int

    def __repr__(self) -> str:
        return f"({self.x},{self.y})"


def up(p: Point) -> Point:
    return Point(p.x, p.y+1)

def down(p: Point) -> Point:
    return Point(p.x, p.y-1)

def right(p: Point) -> Point:
    return Point(p.x+1, p.y)

def left(p: Point) -> Point:
    return Point(p.x-1, p.y)


START_END_CHARS = {ord("S"), ord("E")}


def print_path(end: Point, start: Point, prev: dict[Point, Point], x_len: int, y_len: int) -> None: 
    p = end
    display = [ ["." for _ in range(y_len)] for _ in range(x_len) ]
    display[p.x][p.y] = "E"
    path = [p]
    while p != start:
        n = prev[p]
        c = "."
        if n == up(p):
            c = "<"
        elif n == down(p):
            c = ">"
        elif n == left(p):
            c = "v"
        else:
            c = "^"
        display[n.x][n.y] = c
        path.append(n)
        p = n
    display[start.x][start.y] = "S"
    print()
    for line in display:
        print(f"{''.join(line)}")


def can_traverse(start: Point, end: Point, graph: list[str]) -> bool:
    if end.x < 0 or end.x >= len(graph) or end.y < 0 or end.y >= len(graph[0]):
        return False
    start_val = ord(graph[start.x][start.y])
    end_val = ord(graph[end.x][end.y])
    if start_val in START_END_CHARS:
        start_val = ord("z")
    elif end_val in START_END_CHARS:
        end_val = ord("a")
    return start_val - end_val <= 1


def shortest_path(graph: list[str], start: Point, ends: list[Point]) -> int:
    dist = {start: 0}
    prev = {}
    queue = []

    x_len = len(graph)
    y_len = len(graph[0])
    for x in range(x_len):
        for y in range(y_len):
            p = Point(x, y)
            if p != start:
                dist[p] = 69696969696969
                prev[p] = None
    heapq.heappush(queue, (dist[start], start))

    seen = set()
    seen_chars = set()
    while queue:
        _, current_point = heapq.heappop(queue)
        seen.add(current_point)
        seen_chars.add(graph[current_point.x][current_point.y])
        for direction in [up, down, right, left]:
            next_point = direction(current_point)
            if can_traverse(current_point, next_point, graph):
                new_distance = dist[current_point] + 1
                if new_distance < dist[next_point]:
                    dist[next_point] = new_distance
                    prev[next_point] = current_point
                    if not next_point in set([q_point[1] for q_point in queue]):
                        heapq.heappush(queue, (new_distance, next_point))
                # print_path(next_point, start, prev, x_len, y_len)

    seen_display = [ ["." for _ in range(y_len)] for _ in range(x_len) ]
    for x in range(x_len):
        for y in range(y_len):
            if Point(x, y) in seen:
                seen_display[x][y] = "~"
        print(f"{''.join(seen_display[x])}")
    print("".join(sorted(seen_chars)))

    min_dist = 69696969
    min_point = None
    for end in ends:
        if dist[end] < min_dist:
            min_point = end
            min_dist = dist[end]

    if not min_point:
        raise ValueError("wow no path u dingus")
    print_path(min_point, start, prev, x_len, y_len)
    return min_dist


def main() -> None:
    graph = []
    with file_input() as file:
        while line := file.readline().strip():
            graph.append(line)

    start, end = None, None
    all_a = []
    for x, line in enumerate(graph):
        print(f"{line}")
        for y, elevation in enumerate(line):
            if elevation == "S":
                start = Point(x, y)
            elif elevation == "E":
                end = Point(x, y)
            elif elevation == "a":
                all_a.append(Point(x, y))
    all_a.append(start)

    print(f"\n{start=}, {end=}\n")
    steps = shortest_path(graph, end, [start])
    print(f"\n{steps=}")

    athletic_steps = shortest_path(graph, end, all_a)
    print(f"\n{athletic_steps=}")


if __name__ == "__main__":
    main()