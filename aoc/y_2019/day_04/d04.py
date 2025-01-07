from collections import Counter
from itertools import pairwise

from aoc.cli import file_input


def meets_password_criteria_p2(password: int) -> bool:
    pass_str = str(password)
    for a, b in pairwise(str(password)):
        if b < a:
            return False

    char_count = Counter(pass_str)
    return 2 in set(char_count.values())


def meets_password_criteria_p1(password: int) -> bool:
    found_double = False
    for a, b in pairwise(str(password)):
        if b < a:
            return False
        if a == b:
            found_double = True

    return found_double


def main() -> None:
    lower_bound = upper_bound = 0
    with file_input() as file:
        line = file.readline().strip().split("-")
        lower_bound = int(line[0])
        upper_bound = int(line[1])

    p1 = 0
    p2 = 0

    for password in range(lower_bound, upper_bound + 1):
        if meets_password_criteria_p1(password):
            p1 += 1
        if meets_password_criteria_p2(password):
            p2 += 1

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
