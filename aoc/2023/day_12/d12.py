from aoc.cli import file_input

# from itertools import combinations


def backtrack(
    record: list, idx: int, placing: int, to_place: list[int], results: set
) -> int:
    # print(f"- {idx=}, {placing=}, {to_place} -> {''.join(record)}")
    if (idx + to_place[placing] > len(record)) or (idx > 0 and record[idx - 1] == "#"):
        return 0

    for i in range(to_place[placing]):
        if record[idx + i] == ".":
            return 0

    for i in range(to_place[placing]):
        record[idx + i] = "#"

    if placing == len(to_place) - 1:
        if all(c != "#" for c in record[(idx + to_place[placing]) :]):
            result = "".join(c if c != "?" else "." for c in record)
            results.add(result)
            # print(result)
            return 1
        else:
            return 0

    idx += to_place[placing]
    if idx >= len(record) or record[idx] == "#":
        return 0
    idx += 1

    combos = 0
    placing += 1
    while idx < len(record):
        # print(f" - {idx} -> {placing}")
        to_add = backtrack(record.copy(), idx, placing, to_place, results)
        if to_add == 0 and record[idx] == "#":
            break
        combos += to_add
        idx += 1

    return combos


def compare(mask: list[str], results: set[str], vals: int) -> set[str]:
    valid = set()
    for result in results:
        im_valid = True

        if len(list(filter(None, result.split(".")))) != vals:
            continue
        for i in range(len(mask)):
            if mask[i] != result[i]:
                if mask[i] == "." or (mask[i] == "#" and result[i] == "."):
                    im_valid = False
                    break
        if im_valid:
            valid.add(result)
    return valid


def main() -> None:
    records = []
    with file_input() as file:
        while line := file.readline().strip():
            record = line.split()
            values = list(map(int, record[1].split(",")))
            records.append((record[0], values, len(record[0]) - sum(values)))

    total_arrangements = 0
    for record, values, empty_space in records:
        arrangements = 0
        results = set()
        for i in range(len(record)):
            arrangements += backtrack(list(record), i, 0, values, results)
        valid = compare(record, results, len(values))
        print(f"\n{len(valid)}, {len(results)} -> {''.join(record)}, {values}")
        print("\n".join(results - valid))
        total_arrangements += len(valid)
    print(f"part 1: {total_arrangements}")

    # total_arrangements = 0
    # for record, values, empty_space in records:
    #     big_record = record
    #     big_values = values
    #     for i in range(4):
    #         big_record += "?" + record
    #         big_values.extend(values)

    #     arrangements = 0
    #     results = set()
    #     print(list(big_record), big_values)
    #     for i in range(len(big_record)):
    #         arrangements += backtrack(list(big_record), i, 0, big_values, results)
    #     valid = compare(big_record, results, len(big_values))
    #     print(f"\n{len(valid)}, {len(results)} -> {''.join(big_record)}, {big_values}")
    #     print("\n".join(results-valid))
    #     total_arrangements += len(valid)
    # print(f"part 2: {total_arrangements}")


if __name__ == "__main__":
    main()
