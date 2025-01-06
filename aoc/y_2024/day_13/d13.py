import re

from aoc.cli import file_input
from aoc.geometry import Point, determinant


def solve(prize: Point, a: Point, b: Point) -> int:
    """
    Cramer's rule
    a.x * a_press + b.x * b_press = prize.x
    a.y * a_press + b.y * b_press = prize.y

    |a.x b.x||a_press|   |prize.x|
    |a.y b.y||b_press| = |prize.y|
    """
    a_b_det = determinant(a, b)
    if determinant == 0:
        return -1

    prize_b_det = determinant(prize, b)
    a_prize_det = determinant(a, prize)

    if prize_b_det % a_b_det != 0 or a_prize_det % a_b_det != 0:
        # We only want integer solutions.
        return -1

    a_press = prize_b_det // a_b_det
    b_press = a_prize_det // a_b_det
    return a_press * 3 + b_press


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
    p2 = 0
    mover = Point(10000000000000, 10000000000000)
    for a, b, prize in games:
        p1_cost = solve(prize, a, b)
        if 0 < p1_cost <= 400:
            p1 += p1_cost

        p2_cost = solve(
            prize.move(mover),
            a,
            b,
        )
        if p2_cost != -1:
            p2 += p2_cost

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
