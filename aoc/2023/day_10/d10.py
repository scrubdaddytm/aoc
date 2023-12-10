from aoc.cli import file_input
from dataclasses import dataclass
from aoc.geometry import Point, up, down, left, right, in_bounds, DIRECTIONS, distance, CARDINAL_DIRECTIONS
from aoc.data_structures import PriorityQueue
from aoc.print_tools import print_point_grid, print_grid


PIPE_DIRECTIONS = {
    "L": {right, up},
    "J": {left, up},
    "7": {left, down},
    "F": {right, down},
    "|": {up, down},
    "-": {left, right},
    ".": {},
    "S": {up, down, left, right},
}

VALID_NEIGHBORS = {
    up: {"|", "7", "F"},
    down: {"|", "L", "J"},
    right: {"-", "7", "J"},
    left: {"-", "L", "F"},
}

PRETTY_PIPES = {
    "L": "└",
    "J": "┘",
    "7": "┐",
    "F": "┌",
    "|": "|",
    "-": "-",
    "S": "S",
}

DEFAULT_DISTANCE = 999999999999999


def traverse_graph(
    pipes: dict[Point, chr]
) -> tuple[dict[Point, int], dict[Point, Point]]:
    pq = PriorityQueue(pq_removed_item=Point(-9999999999, -9999999999))
    prev = {}
    distance = {}
    start = None

    for point, pipe in pipes.items():
        prev[point] = None
        distance[point] = DEFAULT_DISTANCE
        if pipe == "S":
            start = point
            pq.add(point, 0)
            distance[point] = 0

    valid_directions = set()
    for direction in CARDINAL_DIRECTIONS:
        next_p = direction(start)
        if pipes.get(next_p, ".") in VALID_NEIGHBORS[direction]:
            valid_directions.add(direction)

    if valid_directions == {up, down}:
        pipes[start] = "|"
    elif valid_directions == {up, right}:
        pipes[start] = "L"
    elif valid_directions == {down, left}:
        pipes[start] = "7"
    elif valid_directions == {down, right}:
        pipes[start] = "F"

    while pq:
        vertex = pq.pop()
        current_pipe_type = pipes[vertex]
        # print(f"{vertex=} == {current_pipe_type}")
        for direction in PIPE_DIRECTIONS[current_pipe_type]:
            next_v = direction(vertex)
            pipe_type = pipes.get(next_v, ".")

            # print(f" - {direction.__name__} -> {next_v=} == {pipe_type},  VALID: {VALID_NEIGHBORS[direction]}")
            if pipe_type not in VALID_NEIGHBORS[direction]:
                continue
            alt_dist = distance[vertex] + 1
            if alt_dist < distance.get(next_v, DEFAULT_DISTANCE):
                distance[next_v] = alt_dist
                prev[next_v] = vertex
                pq.add(next_v, alt_dist)

    return distance, prev


def find_path(start: Point, end: Point, pipes: dict[Point, chr]) -> bool:
    seen = set()
    pq = PriorityQueue(pq_removed_item=Point(-9999999999, -9999999999))
    pq.add(start, distance(start, end))
    while pq:
        p = pq.pop()
        for direction in DIRECTIONS:
            next_p = direction(p)
            if next_p == end:
                return True
            if next_p not in seen and next_p not in pipes:
                pq.add(next_p, distance(next_p, end))
                seen.add(next_p)
    return False


def main() -> None:
    pipes = {}
    size_x = 0
    size_y = 0
    with file_input() as file:
        y = 0
        while line := file.readline().strip():
            for x, pipe in enumerate(line):
                if pipe == ".":
                    continue
                pipes[Point(x, y)] = pipe
            y -= 1
            size_x = len(line)
        size_y = y

    distance, prev = traverse_graph(pipes)

    sanitized_pipes = {}
    for k, v in distance.items():
        if v == DEFAULT_DISTANCE:
            continue
        sanitized_pipes[k] = PRETTY_PIPES[pipes[k]]

    max_dist = 0
    for dist in distance.values():
        if dist == DEFAULT_DISTANCE:
            continue
        max_dist = max(dist, max_dist)

    print(f"Part 1: {max_dist}")


    print_grid(
        sanitized_pipes,
        min_x=0,
        max_x=size_x - 1,
        min_y=size_y + 1,
        max_y=0,
        invert_y=True,
        default_str = " ",
    )

    in_x = set()

    for y in range(abs(size_y)):
        seen_x = []
        for x in range(size_x):
            p = Point(x, -y)
            dist = distance.get(p, DEFAULT_DISTANCE)
            if dist != DEFAULT_DISTANCE:
                pipe = pipes[p]
                if pipe in {"|", "L", "F", "S"}:
                    seen_x.append(pipe)
                elif pipe == "J" and seen_x[-1] == "L":
                    seen_x.pop()
                elif pipe == "7" and seen_x[-1] == "F":
                    seen_x.pop()

            elif len(seen_x) % 2 == 1:
                in_x.add(p)
    print_point_grid(
        in_x, min_x=0, max_x=size_x - 1, min_y=size_y + 1, max_y=0, invert_y=True
    )
    print(f"Part 2: {len(in_x)}")


if __name__ == "__main__":
    main()
