from dataclasses import dataclass
from aoc.cli import file_input


@dataclass(frozen=True)
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

DIRECTIONS = {
    "U": up,
    "D": down,
    "R": right,
    "L": left,
}


def follow(head: Point, tail: Point) -> Point:
    x_diff = tail.x - head.x
    y_diff = tail.y - head.y

    if abs(x_diff) <= 1 and abs(y_diff) <= 1:
        return tail
    else:
        return Point(
            head.x if abs(x_diff) == 1 else head.x + (x_diff//2),
            head.y if abs(y_diff) == 1 else head.y + (y_diff//2),
        )


def move(moves: list[str, str], tail_length: int) -> tuple[set[Point], set[int], set[int]]:
    seen = set()
    seen_x = set()
    seen_y = set()

    worm = [Point(0,0) for _ in range(tail_length+1)]
    for move in moves:
        direction = DIRECTIONS[move[0]]
        count = int(move[1])

        for _ in range(count):
            worm[0] = direction(worm[0])
            for idx, tail in enumerate(worm[1:], 1):
                worm[idx] = follow(worm[idx-1], tail)

            seen.add(worm[-1])
            seen_x.add(worm[-1].x)
            seen_y.add(worm[-1].y)

    return seen, seen_x, seen_y


def print_points(points: set[Point], seen_x: set[int], seen_y: set[int]) -> None:
    min_x, max_x = min(seen_x), max(seen_x)
    min_y, max_y = min(seen_y), max(seen_y)

    grid = [["." for _ in range(max_x - min_x)] for _ in range(max_y - min_y)]
    for x in range(max_x - min_x):
        for y in range(max_y - min_y):
            if Point(x+min_x, y+min_y) in points:
                grid[len(grid)-y-1][x] = "#"

    grid[len(grid)-1+min_y][0-min_x] = "s"
    start_y = max_y
    for row in grid:
        print(f"{start_y:^3} - {''.join(row)}")
        start_y -= 1


def main() -> None:
    moves = []
    with file_input() as file:
        while line := file.readline().strip().split():
            moves.append(line)

    for tail_length in [1, 9]:
        tail_seen, seen_x, seen_y = move(moves, tail_length)

        print_points(tail_seen, seen_x, seen_y)
        print(f"SEEN = {len(tail_seen)}")
        print("\n\n")


if __name__ == "__main__":
    main()
