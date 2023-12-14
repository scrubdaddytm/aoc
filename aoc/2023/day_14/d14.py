from aoc.cli import file_input
from aoc.geometry import up, down, left, right, Point, in_bounds
from aoc.print_tools import print_grid


DIRECTIONS = {
    "north": down,
    "south": up,
    "east": right,
    "west": left,
}


def move(graph: dict[Point, chr], c_dir: str, bound_x: int, bound_y: int) -> None:
    direction = DIRECTIONS[c_dir]

    if c_dir in {"north", "south"}:
        start_y = end_y = step = 0
        r_end_y = 0
        if c_dir == "north":
            end_y = bound_y
            r_end_y = -1
            step = 1
        else:
            start_y = bound_y
            r_end_y = start_y
            end_y = -1
            step = -1
        for y in range(start_y, end_y, step):
            for x in range(bound_x):
                for y_dir in range(y, r_end_y, -step):
                    rock_point = Point(x, y_dir)
                    rock = graph.get(rock_point)
                    if rock != "O":
                        continue
                    next_point = direction(rock_point)
                    if in_bounds(next_point, max_x=bound_x, max_y=bound_y) and not graph.get(next_point):
                        graph.pop(rock_point)
                        graph[next_point] = "O"
    else:
        start_x = end_x = step = 0
        r_end_x = 0
        if c_dir == "east":
            end_x = bound_x
            r_end_x = -1
            step = 1
        else:
            start_x = bound_x
            r_end_x = bound_x
            end_x = -1
            step = -1
        for x in range(start_x, end_x, step):
            for y in range(bound_y):
                for x_dir in range(x, r_end_x, -step):
                    rock_point = Point(x_dir, y)
                    rock = graph.get(rock_point)
                    if rock != "O":
                        continue
                    next_point = direction(rock_point)
                    if in_bounds(next_point, max_x=bound_x, max_y=bound_y) and not graph.get(next_point):
                        graph.pop(rock_point)
                        graph[next_point] = "O"


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

    print_grid(graph)

    p1_copy_graph = graph.copy()
    move(p1_copy_graph, "north", x, y)

    print(f"Part 1: {load(p1_copy_graph, 'north', x, y)}")

    seen_states = set()
    state_pos = {}
    state = frozenset(graph.keys())

    cycle_count = 0
    while state not in seen_states:
        seen_states.add(state)
        state_pos[state] = cycle_count
        cycle(graph, x, y)
        state = frozenset(graph.items())
        cycle_count += 1

    cycle_start_val = state_pos[state]

    cycle_len = cycle_count - cycle_start_val
    print(f"{cycle_start_val=}, {cycle_len=}")

    cycle_offset = (1_000_000_000 - cycle_start_val) % cycle_len
    print(f"{cycle_offset=}")

    for k, v in state_pos.items():
        if v == cycle_start_val + cycle_offset:
            state_dict = {item[0]: item[1] for item in k}
            print(f"Part 2: {load(state_dict, 'north', x, y)}")
            break


if __name__ == "__main__":
    main()
