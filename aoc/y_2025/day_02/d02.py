from itertools import batched

from aoc.cli import file_input

"""
11-22 still has two invalid IDs, 11 and 22.
95-115 now has two invalid IDs, 99 and 111.
998-1012 now has two invalid IDs, 999 and 1010.
1188511880-1188511890 still has one invalid ID, 1188511885.
222220-222224 still has one invalid ID, 222222.
1698522-1698528 still contains no invalid IDs.
446443-446449 still has one invalid ID, 446446.
38593856-38593862 still has one invalid ID, 38593859.
565653-565659 now has one invalid ID, 565656.
824824821-824824827 now has one invalid ID, 824824824.
2121212118-2121212124 now has one invalid ID, 2121212121.
"""


def find_invalid(i: int) -> bool:
    i_str = str(i)
    str_len = len(i_str)
    for repeat in range(1, (str_len // 2) + 1):
        if str_len % repeat != 0:
            continue
        seen = set(["".join(batch) for batch in batched(i_str, repeat)])
        # print(f"{i}: {repeat} -> {seen}{'<-------------' if len(seen) == 1 else ''}")
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

            bad = find_invalid(i)
            if bad:
                p2 += i

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
