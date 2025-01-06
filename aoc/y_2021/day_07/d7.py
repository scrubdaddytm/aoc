from aoc.cli import file_input
from dataclasses import dataclass
from statistics import median, mean


def p2_fuel_calc(positions: list[int], move_to: int) -> int:
    p2_fuel = 0
    for position in positions:
        dist = abs(position - move_to)
        p2_fuel += int(((dist * (dist + 1)) / 2))
    return p2_fuel


def main() -> None:
    positions = []
    with file_input() as file:
        while line := file.readline().strip():
            positions = list(map(int, line.split(",")))
    print(f"{positions}")

    print(f"unrounded median {median(positions)}")
    med_loc = round(median(positions))
    p1_fuel = 0
    for position in positions:
        p1_fuel += abs(position - med_loc)

    print(f"part 1: moved to {med_loc} and cost {p1_fuel}")

    print(f"unrounded mean {mean(positions)}")
    mean_loc = round(mean(positions))

    p2_fuel = p2_fuel_calc(positions, mean_loc)
    new_loc = mean_loc
    new_loc_dec = mean_loc
    while (new_fuel := p2_fuel_calc(positions, new_loc_dec-1)) < p2_fuel:
        new_loc_dec -= 1
        p2_fuel = new_fuel
        new_loc = new_loc_dec

    new_loc_inc = mean_loc
    while (new_fuel := p2_fuel_calc(positions, new_loc_inc+1)) < p2_fuel:
        new_loc_inc += 1
        p2_fuel = new_fuel
        new_loc = new_loc_inc

    print(f"part 2: moved to {new_loc} and cost {p2_fuel}")


if __name__ == "__main__":
    main()
