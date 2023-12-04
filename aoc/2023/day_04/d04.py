from aoc.cli import file_input


def main() -> None:
    lines = []
    with file_input() as file:
        while line := file.readline().strip():
            lines.append(line.split(": "))
            lines[-1][1] = lines[-1][1].split(" | ")
            winners = set(map(int, lines[-1][1][0].split()))
            lines[-1][1][0] = winners
            picked = set(map(int, lines[-1][1][1].split()))
            lines[-1][1][1] = picked

    points = 0
    card_count = {k: 1 for k in range(len(lines))}
    for game_num, game in enumerate(lines):
        for card_idx in range(card_count[game_num]):
            winners = game[1][0]
            picked = game[1][1]
            winning_numbers = len(winners & picked)
            if card_idx == 0:
                points += int(2 ** (winning_numbers - 1))
            for card_increase in range(game_num + 1, game_num + winning_numbers + 1):
                card_count[card_increase] += 1
    print(f"part 1: {points=}")
    print(f"part 2: {sum(card_count.values())}")


if __name__ == "__main__":
    main()
