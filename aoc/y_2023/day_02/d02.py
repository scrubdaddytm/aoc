from aoc.cli import file_input
from collections import defaultdict
import math


MAX_BALLS = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def main() -> None:
    games = []
    with file_input() as file:
        while line := file.readline().strip():
            games.append(line.split(": "))
            pulls = []
            for pull in games[-1][1].split("; "):
                pulls.append(pull.split(", "))
            games[-1][1] = pulls

    valid_games = set()
    game_power = 0
    for game in games:
        _, game_number = game[0].split(" ")
        rnd = game[1]
        valid = True
        min_balls_needed = defaultdict(int)
        for balls in rnd:
            for ball in balls:
                num, color = ball.split(" ")
                num = int(num)
                if num > MAX_BALLS[color]:
                    valid = False
                min_balls_needed[color] = max(num, min_balls_needed[color])
        game_power += math.prod(min_balls_needed.values())
        if valid:
            valid_games.add(int(game_number))

    print(f"round 1: {sum(valid_games)}")
    print(f"round 2: {game_power}")


if __name__ == "__main__":
    main()
