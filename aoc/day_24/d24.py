from dataclasses import dataclass
from collections import deque
import heapq
from aoc.cli import file_input
from aoc.geometry import Point
from aoc.geometry import up
from aoc.geometry import down
from aoc.geometry import left
from aoc.geometry import right


DIRS = {
    "^": up,
    "v": down,
    "<": left,
    ">": right,
}


def nowhere(p: Point) -> Point:
    return p


def print_state(blizzard_state: dict[Point, list[str]], grid_size: tuple[int, int], me: Point | None = None) -> None:
    print(f"#{'E' if me and me.y == -1 else '.'}{'#'*(grid_size[0])}")
    for y in range(grid_size[1]):
        line = "#"
        for x in range(grid_size[0]):
            dirs = blizzard_state.get(Point(x, y), [])
            if Point(x, y) == me:
                line += "E"
            elif len(dirs) > 1:
                line += str(len(dirs))
            elif len(dirs) == 1:
                line += dirs[0]
            else:
                line += "."
        print(f"{line}#")
    print(f"{'#'*(grid_size[0])}{'E' if me and me.x == grid_size[0] else '.'}#\n")


state_cache = {}
def get_state(blizzards: dict[Point, str], minute: int, grid_size: tuple[int, int]) -> dict[Point, list[str]]:
    next_blizz_locs = {}
    if minute in state_cache:
        return state_cache[minute]
    for blizz, direction in blizzards.items():
        next_blizz = None
        if direction == "^":
            next_blizz = Point(blizz.x, (blizz.y - minute) % grid_size[1])
        elif direction == "v":
            next_blizz = Point(blizz.x, (blizz.y + minute) % grid_size[1])
        elif direction == "<":
            next_blizz = Point((blizz.x - minute) % grid_size[0], blizz.y)
        elif direction == ">":
            next_blizz = Point((blizz.x + minute) % grid_size[0], blizz.y)
        dirs = next_blizz_locs.setdefault(next_blizz, [])
        dirs.append(direction)
        next_blizz_locs[next_blizz] = dirs
    state_cache[minute] = next_blizz_locs
    return next_blizz_locs


def can_traverse(p: Point, blizz_state: dict[Point, list[str]], grid_size: tuple[int, int], start: Point, end: Point):
    return any(
        [
            all(
                [
                    0 <= p.x < grid_size[0],
                    0 <= p.y < grid_size[1],
                    p not in blizz_state,
                ]
            ),
            p == start,
            p == end,
        ]
    )


def traverse(
    blizzards: dict[Point, str],
    grid_size: tuple[int, int],
    start: Point,
    end: Point,
    start_time=0,
) -> int:
    q = []
    q.append((start.distance(end), start_time, start))
    seen = set()
    best_dist = 6969696969
    print(f"{start} -> {end}, {start_time=}")
    while q:
        d, m, p = heapq.heappop(q)
        if (p, m) in seen:
            continue
        seen.add((p, m))
        if p == end:
            best_dist = min(best_dist, m)
            print(f"{best_dist=}")
            continue
        elif m > best_dist:
            continue
        blizz_state = get_state(blizzards, m + 1, grid_size)
        # print_state(blizz_state, grid_size, p)
        for d in [right, down, up, left, nowhere]:
            next_p = d(p)
            if not can_traverse(next_p, blizz_state, grid_size, start, end) and not (next_p, m + 1) in seen:
                continue

            time_remaining = best_dist - m - 1
            next_dist = next_p.distance(end)

            if time_remaining <= 0 or next_dist >= time_remaining:
                continue

            heapq.heappush(q, (next_p.distance(end), m + 1, next_p))

    return best_dist


def main() -> None:
    blizzards = {}
    with file_input() as file:
        x_len = len(file.readline().strip()) - 2
        y_len = -1
        while line := file.readline():
            y_len += 1
            for x, point in enumerate(line[1:-1]):
                if point == "#":
                    break
                if point == ".":
                    continue
                blizzards[Point(x, y_len)] = point
    grid_size = (x_len, y_len)
    max_states = x_len * y_len
    global state_cache
    state_cache = {}

    start = Point(0, -1)
    end = Point(grid_size[0] - 1, grid_size[1])

    print(f"Grid Size: {grid_size}, Max States: {max_states}")

    time = traverse(blizzards, grid_size, start, end)
    print(f"Part 1: {time}")

    time_back = traverse(blizzards, grid_size, end, start, time)
    print(f"{time_back=}")
    final_time = traverse(blizzards, grid_size, start, end, time_back)
    print(f"Part 2: {final_time=}. back={time_back-time}, again={final_time-time_back}")


if __name__ == "__main__":
    main()
