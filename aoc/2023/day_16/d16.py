from aoc.cli import file_input
from aoc.geometry import Point, up, down, left, right, in_bounds
from aoc.print_tools import print_point_grid, print_grid


MODIFIERS = {
    "\\": {
        right: [up],
        up: [right],
        down: [left],
        left: [down],
    },
    "/": {
        right: [down],
        down: [right],
        left: [up],
        up: [left],
    },
    "|": {
        right: [up, down],
        left: [up, down],
        up: [up],
        down: [down],
    },
    "-": {
        right: [right],
        left: [left],
        up: [left, right],
        down: [left, right],
    },
}


def energize(graph: dict[Point, chr], bound_x: int, bound_y: int, start: Point, direction: callable) -> set[Point]:
    queue = [(start, direction)]
    seen = set()
    energized = set()

    while queue:
        p, d = queue.pop()
        if (p, d) in seen:
            continue
        seen.add((p, d))

        if not in_bounds(p, max_x=bound_x, max_y=bound_y):
            continue

        energized.add(p)
        item = graph.get(p)
        if not item:
            queue.append((d(p), d))
        else:
            new_dirs = MODIFIERS[item][d]
            for new_dir in new_dirs:
                queue.append((new_dir(p), new_dir))

    return energized


def main() -> None:
    graph = {}
    bound_y = 0
    bound_x = 0
    with file_input() as file:
        while line := file.readline().strip():
            bound_x = len(line)
            for x, c in enumerate(line):
                if c != ".":
                    graph[Point(x, bound_y)] = c
            bound_y += 1

    energized = energize(graph, bound_x, bound_y, Point(0, 0), right)
    print_grid(graph)
    print_point_grid(energized)

    print(f"Part 1: {len(energized)}")

    max_energy = len(energized)
    for x in range(bound_x):
        en_up = energize(graph, bound_x, bound_y, Point(x, 0), up)
        en_down = energize(graph, bound_x, bound_y, Point(x, bound_y-1), down)
        max_energy = max(max_energy, len(en_up), len(en_down))
    for y in range(bound_y):
        en_right = energize(graph, bound_x, bound_y, Point(0, y), right)
        en_left = energize(graph, bound_x, bound_y, Point(bound_x-1, y), left)
        max_energy = max(max_energy, len(en_right), len(en_left))

    print(f"Part 2: {max_energy}")


if __name__ == "__main__":
    main()
