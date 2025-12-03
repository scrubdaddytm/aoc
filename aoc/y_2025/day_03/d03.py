from aoc.cli import file_input


def best(bank: list[int], count: int = 2) -> int:
    result = 0
    start = 0
    for i in range(count):
        best = 0
        best_idx = 0
        for j in range(start, len(bank) - ((count - 1) - i)):
            if bank[j] > best:
                best = bank[j]
                best_idx = j
            if best == 9:
                break
        result *= 10
        result += best
        start = best_idx + 1
    return result


def find_da_best(banks: list[list[int]], count: int = 2) -> int:
    result = 0
    for bank in banks:
        result += best(bank, count)
    return result


def main() -> None:
    banks = []
    with file_input() as file:
        while line := file.readline().strip():
            banks.append(list(map(int, line)))

    p1 = find_da_best(banks)
    p2 = find_da_best(banks, 12)

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
