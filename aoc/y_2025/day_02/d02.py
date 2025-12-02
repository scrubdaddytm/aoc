from itertools import batched

from aoc.cli import file_input


def find_invalid(i: int) -> bool:
    i_str = str(i)
    for repeat in range(1, (len(i_str) // 2) + 1):
        if len(i_str) % repeat != 0:
            continue
        seen = set(["".join(batch) for batch in batched(i_str, repeat)])
        if len(seen) == 1:
            return True

    return False


def main() -> None:
    ranges = []
    with file_input() as file:
        line = file.readline().strip()
        raw_ranges = line.split(",")
        for id_range in raw_ranges:
            ranges.append(id_range.split("-"))
    print(f"{ranges}")

    p1 = 0
    p2 = 0

    for lb, ub in ranges:
        start = int(lb)
        end = int(ub)
        for i in range(start, end + 1):
            i_str = str(i)
            if i_str[len(i_str) // 2:] == i_str[: len(i_str) // 2]:
                p1 += i
                p2 += i
            elif find_invalid(i):
                p2 += i

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
