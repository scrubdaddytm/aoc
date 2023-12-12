from aoc.cli import file_input
from functools import cache


@cache
def backtrack(
    record: str,
    idx: int,
    placing: int,
    to_place: tuple[int],
) -> int:
    value = to_place[placing]
    if (idx + value > len(record)) or any(c == "." for c in record[idx: idx + value]):
        return 0

    if placing == len(to_place) - 1:
        if all(c != "#" for c in record[(idx + value):]):
            return 1
        else:
            return 0

    idx += value
    if idx >= len(record) or record[idx] == "#":
        return 0

    idx += 1

    combos = 0
    placing += 1
    while idx < len(record):
        result = backtrack(record, idx, placing, to_place)
        combos += result
        if record[idx] == "#":
            break
        idx += 1

    return combos


def start_backtracking(record: str, values: tuple[int]) -> set[str]:
    result = 0
    for i in range(len(record)):
        result += backtrack(record, i, 0, values)
        if record[i] == "#":
            break
    return result


def main() -> None:
    records = []
    with file_input() as file:
        while line := file.readline().strip():
            record = line.split()
            values = tuple(map(int, record[1].split(",")))
            records.append((record[0], values, len(record[0]) - sum(values)))

    total_arrangements = 0
    for record, values, empty_space in records:
        total_arrangements += start_backtracking(record, values)
    print(f"part 1: {total_arrangements}")

    total_arrangements = 0
    for record, values, empty_space in records:
        big_record = record
        big_values = list(values)
        for i in range(4):
            big_record += "?" + record
            big_values.extend(values)

        total_arrangements += start_backtracking(big_record, tuple(big_values))
    print(f"part 2: {total_arrangements}")


if __name__ == "__main__":
    main()
