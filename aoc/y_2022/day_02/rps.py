from aoc.cli import file_input
from dataclasses import dataclass
from dataclasses import field


@dataclass(frozen=True)
class Pair:
    them: str
    me: str


HANDS = {
    "A": "R",
    "B": "P",
    "C": "S",
}
ALL_PAIRS = {
    Pair("R", "R"): 1+3,
    Pair("R", "P"): 2+6,
    Pair("R", "S"): 3+0,
    Pair("P", "R"): 1+0,
    Pair("P", "P"): 2+3,
    Pair("P", "S"): 3+6,
    Pair("S", "R"): 1+6,
    Pair("S", "P"): 2+0,
    Pair("S", "S"): 3+3,
}
WINS = {
    "R": Pair("R", "P"),
    "P": Pair("P", "S"),
    "S": Pair("S", "R"),
}
LOSSES = {
    "R": Pair("R", "S"),
    "P": Pair("P", "R"),
    "S": Pair("S", "P"),
}
DRAWS = {
    "R": Pair("R", "R"),
    "P": Pair("P", "P"),
    "S": Pair("S", "S"),
}


def fight(rounds: list[Pair]) -> int:
    total_points = 0
    for round in rounds:
        if round.me == "R":
            total_points += ALL_PAIRS[LOSSES[round.them]]
        elif round.me == "P":
            total_points += ALL_PAIRS[DRAWS[round.them]]
        else:
            total_points += ALL_PAIRS[WINS[round.them]]
    return total_points


def main() -> None:
    normalizer = ord("X")-ord("A")
    rounds = []
    with file_input() as file:
        while line := file.readline():
            round = line.split()
            rounds.append(Pair(HANDS[round[0]], HANDS[chr(ord(round[1])-normalizer)]))

    total_points = fight(rounds)
    print(f"{total_points}")

if __name__ == "__main__":
    main()