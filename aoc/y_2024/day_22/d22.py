from collections import defaultdict, deque
from functools import cache

from aoc.cli import file_input


@cache
def secret_number(num: int) -> int:
    m = num * 64
    num ^= m
    num %= 16777216
    d = num // 32
    num ^= d
    num %= 16777216
    m2 = num * 2048
    num ^= m2
    num %= 16777216
    return num


def main() -> None:
    secret_numbers = []
    with file_input() as file:
        while line := file.readline().strip():
            secret_numbers.append(int(line))

    p1 = 0
    p2 = 0

    seent = defaultdict(int)
    for buyer in secret_numbers:
        locally_seent = set()
        diff = deque(maxlen=4)
        last_price = buyer % 10
        for i in range(2000):
            new_num = secret_number(buyer)
            price = new_num % 10

            diff.append(price - last_price)

            diff_tuple = tuple(diff)
            if diff_tuple not in locally_seent:
                seent[diff_tuple] += price
                locally_seent.add(diff_tuple)

            last_price = price
            buyer = new_num
        p1 += buyer

    p2 = 0
    for v in seent.values():
        p2 = max(p2, v)

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
