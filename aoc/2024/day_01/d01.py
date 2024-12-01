from aoc.cli import file_input
from collections import Counter


def main() -> None:
    location_list_left = []
    location_list_right = []
    with file_input() as file:
        while line := file.readline().split():
            location_list_left.append(int(line[0]))
            location_list_right.append(int(line[1]))

    location_list_left = sorted(location_list_left)
    location_list_right = sorted(location_list_right)

    diff = 0
    for l, r in zip(location_list_left, location_list_right):
        diff += abs(l - r)

    print(f"Part 1: {diff}")

    right_counter = Counter(location_list_right)

    similarity = 0
    for l in location_list_left:
        similarity += l * right_counter[l]

    print(f"Part 2: {similarity}")


if __name__ == "__main__":
    main()
