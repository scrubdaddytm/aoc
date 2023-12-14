from aoc.cli import file_input
from aoc.geometry import up, down, left, right, Point, in_bounds
from aoc.print_tools import print_grid


DIRECTIONS = {
    "north": down,
    "south": up,
    "east": right,
    "west": left,
}


def move_rock(graph: dict[Point, chr], rock_point: Point, direction: callable, bound_x: int, bound_y: int) -> None:
    rock = graph.get(rock_point)
    if rock != "O":
        return
    next_point = direction(rock_point)
    prev_point = rock_point
    while in_bounds(next_point, max_x=bound_x, max_y=bound_y) and not graph.get(next_point):
        prev_point = next_point
        next_point = direction(next_point)
    if rock_point != prev_point:
        graph.pop(rock_point)
        graph[prev_point] = "O"


def move(graph: dict[Point, chr], c_dir: str, bound_x: int, bound_y: int) -> None:
    direction = DIRECTIONS[c_dir]

    if c_dir in {"north", "south"}:
        start_y = end_y = step = 0
        if c_dir == "north":
            end_y = bound_y
            step = 1
        else:
            start_y = bound_y
            end_y = -1
            step = -1
        for y in range(start_y, end_y, step):
            for x in range(bound_x):
                move_rock(graph, Point(x, y), direction, bound_x, bound_y)
    else:
        start_x = end_x = step = 0
        if c_dir == "west":
            end_x = bound_x
            step = 1
        else:
            start_x = bound_x
            end_x = -1
            step = -1
        for x in range(start_x, end_x, step):
            for y in range(bound_y):
                move_rock(graph, Point(x, y), direction, bound_x, bound_y)


def cycle(graph: dict[Point, chr], bound_x: int, bound_y: int) -> None:
    cycle_dirs = ["north", "west", "south", "east"]
    for c in cycle_dirs:
        move(graph, c, bound_x, bound_y)


def load(graph: dict[Point, chr], c_dir: str, bound_x: int, bound_y: int) -> int:
    load = 0
    for point, rock in graph.items():
        if rock != "O":
            continue
        if c_dir in {"north", "south"}:
            dist = abs(point.y - bound_y)
            load += dist if dist > 0 else 1
        else:
            pass
    return load


def hash_state(graph: dict[Point, chr]) -> str:
    state = ""
    for p, c in sorted(graph.items()):
        state += str(p) + c + ";"
    return state


def state_to_graph(state: str) -> dict[Point, chr]:
    items = state.split(";")
    graph = {}
    for item in items:
        if not item:
            continue
        point, val = item.split(")")
        point = Point(*list(map(int, point[1:].split(","))))
        graph[point] = val
    return graph


def main() -> None:
    graph = {}
    y = 0
    with file_input() as file:
        while line := file.readline().strip():
            x = len(line)
            for x, char in enumerate(line):
                if char != ".":
                    graph[Point(x, y)] = char
            y += 1
    x += 1

    p1_copy_graph = graph.copy()
    move(p1_copy_graph, "north", x, y)

    print(f"Part 1: {load(p1_copy_graph, 'north', x, y)}")

    seen_states = set()
    state_pos = {}
    state = hash_state(graph)

    cycle_count = 0
    while state not in seen_states:
        seen_states.add(state)
        state_pos[state] = cycle_count
        cycle(graph, x, y)
        state = hash_state(graph)
        cycle_count += 1

    cycle_start_val = state_pos[state]

    cycle_len = cycle_count - cycle_start_val
    print(f"{cycle_start_val=}, {cycle_len=}")

    cycle_offset = (1_000_000_000 - cycle_start_val) % cycle_len
    print(f"{cycle_offset=}")

    for k, v in state_pos.items():
        if v == cycle_start_val + cycle_offset:
            final_graph = state_to_graph(k)
            print(f"Part 2: {load(final_graph, 'north', x, y)}")
            break


if __name__ == "__main__":
    main()
