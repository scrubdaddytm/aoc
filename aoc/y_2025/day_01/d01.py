from aoc.cli import file_input


def main() -> None:
    instructions = []
    with file_input() as file:
        while line := file.readline():
            instructions.append((line[0], int(line[1:])))

    p1 = 0
    p2 = 0

    dial = 50
    for direction, count in instructions:
        p2 += count // 100
        count %= 100

        if direction == "L":
            if dial != 0 and dial - count <= 0:
                p2 += 1
            dial -= count
        else:
            dial += count
            if dial >= 100:
                p2 += 1

        dial %= 100
        if dial == 0:
            p1 += 1

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
