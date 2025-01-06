from aoc.cli import file_input


def main() -> None:
    p1 = p2 = 0

    with file_input() as file:
        while line := file.readline().strip():
            mass = int(line)
            fuel_req = (mass // 3) - 2
            p1 += fuel_req

            while fuel_req > 0:
                p2 += fuel_req
                fuel_req = (fuel_req // 3) - 2

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
