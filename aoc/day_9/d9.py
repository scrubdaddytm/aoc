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
    if head == tail:
        # print(f"CASE A")
        return tail
    
    x_diff = tail.x - head.x
    y_diff = tail.y - head.y


    if abs(x_diff) <= 1 and abs(y_diff) <= 1:
        return tail

    if head.x == tail.x:
        # print(f"CASE B")
        return Point(tail.x, head.y + ((tail.y - head.y)//2))
    elif head.y == tail.y:
        # print(f"CASE C")
        return Point((head.x + ((tail.x - head.x)//2)), tail.y)
    else:
        # print(f"CASE D")

        return Point(
            head.x if abs(x_diff) == 1 else head.x + (x_diff//2),
            head.y if abs(y_diff) == 1 else head.y + (y_diff//2),
        )


def move(moves: list[str, str], tail_length: int) -> tuple[set[Point], int, int]:
    max_x = 0
    max_y = 0

    seen = set()
    worm = [Point(0,0) for _ in range(tail_length+1)]
    for move in moves:
        direction = DIRECTIONS[move[0]]
        count = int(move[1])

        for _ in range(count):
            worm[0] = direction(worm[0])
            for idx, tail in enumerate(worm[1:], 1):
                worm[idx] = follow(worm[idx-1], tail)

            seen.add(worm[-1])

            max_x = max(max_x, worm[0].x)
            max_y = max(max_y, worm[0].y)

    return seen, max_x, max_y


def print_points(points: set[Point], grid_size_x: int, grid_size_y: int) -> None:
    """Doesnt work lol negative numbers throw it off"""
    grid = [["." for _ in range(grid_size_x)] for _ in range(grid_size_y)]
    for x in range(grid_size_x):
        for y in range(grid_size_y):
            if Point(x, y) in points:
                grid[len(grid)-y-1][x] = "#"

    for row in grid:
        print(f"{''.join(row)}")


def main() -> None:
    moves = []
    with file_input() as file:
        while line := file.readline().strip().split():
            moves.append(line)

    for tail_length in [1, 9]:
        tail_seen, max_x, max_y = move(moves, tail_length)

        # print_points(tail_seen, max_x, max_y)
        print(f"{len(tail_seen)}")


if __name__ == "__main__":
    main()