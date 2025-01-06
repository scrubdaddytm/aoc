from aoc.cli import file_input_v2
from aoc.data_structures import PriorityQueue
from aoc.geometry import CARDINAL_DIRECTIONS, Point


def shortest_path(walls: set[Point], origin: Point, target: Point) -> set[Point] | None:
    q = PriorityQueue(pq_removed_item=Point(-1, -1))
    q.add(origin, 0)
    dist = {}
    dist[origin] = 0
    prev = {}

    while q:
        p = q.pop()
        if p == target:
            break
        curr_dist = dist[p]

        for d in CARDINAL_DIRECTIONS:
            new_p = d(p)
            if new_p not in walls and (
                new_p not in dist or dist[new_p] > curr_dist + 1
            ):
                dist[new_p] = curr_dist + 1
                prev[new_p] = p
                q.add(new_p, curr_dist + 1)

    if target not in dist:
        return None

    path = set()
    p = target
    while p != origin:
        path.add(p)
        p = prev[p]
    return path


def main() -> None:
    falling_bytes = []
    using_sample = False
    with file_input_v2() as (file, is_sample):
        using_sample = is_sample
        while line := file.readline().strip():
            falling_bytes.append(Point(*map(int, line.split(","))))

    bound = 7 if using_sample else 71
    p1_bytes = 12 if using_sample else 1024
    target = Point(6, 6) if using_sample else Point(70, 70)
    origin = Point(0, 0)

    walls = set()
    for c in range(-1, bound):
        walls.add(Point(c, -1))
        walls.add(Point(c, bound))
        walls.add(Point(-1, c))
        walls.add(Point(bound, c))
    walls.add(Point(bound, bound))

    walls |= set(falling_bytes[:p1_bytes])

    p1_path = shortest_path(walls, origin, target)

    next_wall_idx = p1_bytes

    path = p1_path
    while path:
        while falling_bytes[next_wall_idx] not in path:
            walls.add(falling_bytes[next_wall_idx])
            next_wall_idx += 1

        walls.add(falling_bytes[next_wall_idx])
        next_wall_idx += 1

        path = shortest_path(walls, origin, target)

    p1 = len(p1_path)
    p2 = falling_bytes[next_wall_idx - 1]

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
