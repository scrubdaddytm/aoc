import re

from aoc.cli import file_input
from aoc.geometry import Point


def solve(prize: Point, a: Point, b: Point) -> int:
    """
    Cramer's rule
    a.x * ap + b.x * bp = prize.x
    a.y * ap + b.y * bp = prize.y

    |a.x b.x||ap|   |prize.x|
    |a.y b.y||bp| = |prize.y|
    """
    determinant = a.x * b.y - b.x * a.y
    if determinant == 0:
        return -1

    a_numerator = prize.x * b.y - b.x * prize.y
    b_numerator = a.x * prize.y - prize.x * a.y

    if a_numerator % determinant != 0 or b_numerator % determinant != 0:
        # We only want integer solutions.
        return -1

    ap = a_numerator // determinant
    bp = b_numerator // determinant
    return ap * 3 + bp


def main() -> None:
    games = []
    with file_input() as file:
        current_game = []
        while line := file.readline():
            for _ in range(3):
                x, y = re.findall(r"(\d+)", line)
                current_game.append(Point(int(x), int(y)))
                line = file.readline()
            games.append(current_game)
            current_game = []

    p1 = 0
    for game in games:
        cost = solve(game[2], game[0], game[1])
        if 0 < cost <= 400:
            p1 += cost

    p2 = 0
    for game in games:
        cost = solve(
            game[2].move(Point(10000000000000, 10000000000000)),
            game[0],
            game[1],
        )
        if cost != -1:
            p2 += cost

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
