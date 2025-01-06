from aoc.cli import file_input
from aoc.geometry import up as down
from aoc.geometry import down as up
from aoc.geometry import left, right
from aoc.geometry import Point
from aoc.geometry import in_bounds


ROTATE_DIR = {
    up: right,
    right: down,
    down: left,
    left: up,
}


def traverse(graph, guard, max_x, max_y) -> tuple[set, bool]:
    seen_with_dir = set()
    guard_dir = up

    while in_bounds(guard, max_x, max_y):
        if (guard, guard_dir) in seen_with_dir:
            return seen_with_dir, True
        seen_with_dir.add((guard, guard_dir))
        next_pos = guard_dir(guard)
        if next_pos in graph:
            guard_dir = ROTATE_DIR[guard_dir]
        else:
            guard = next_pos

    return seen_with_dir, False


def main() -> None:
    lines = []
    with file_input() as file:
        while line := file.readline().strip():
            lines.append(line)

    graph = set()
    guard = None

    for i, line in enumerate(lines):
        for j, cell in enumerate(line):
            if cell == "#":
                graph.add(Point(j, i))
            elif cell == "^":
                guard = Point(j, i)

    p1_seen, _ = traverse(graph, guard, len(lines), len(lines[0]))
    p1_seen = {x[0] for x in p1_seen}
    print(f"Part 1: {len(p1_seen)}")

    p2 = 0
    p1_seen.remove(guard)
    for i, p in enumerate(p1_seen):
        graph.add(p)
        _, looped = traverse(graph, guard, len(lines), len(lines[0]))
        if looped:
            p2 += 1
        graph.remove(p)
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
