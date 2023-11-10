from aoc.cli import file_input


def main() -> None:
    fish = []
    with file_input() as file:
        while line := file.readline():
            fish = [int(val) for val in line.strip().split(",")]

    days = [[0, 0] for _ in range(7)]
    for f in fish:
        days[f][0] += 1
    for day in range(256):
        if day == 80:
            print(f"part 1: {sum([day[0]+day[1] for day in days])}")
        today = day % 7
        new_fish_day = (day + 9) % 7

        days[new_fish_day][1] += days[today][0]
        days[today][0] += days[today][1]
        days[today][1] = 0
    print(f"part 2: {sum([day[0]+day[1] for day in days])}")


if __name__ == "__main__":
    main()
