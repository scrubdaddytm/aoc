from aoc.cli import file_input


def main() -> None:
    ranges = []
    ids = []
    with file_input() as file:
        while line := file.readline().strip():
            ranges.append(tuple(map(int, line.split("-"))))
        while line := file.readline().strip():
            ids.append(int(line))

    ranges = sorted(ranges)

    p1 = 0
    p2 = 0

    merged_ranges = [ranges[0]]

    for b in ranges[1:]:
        a = merged_ranges.pop()
        if a[1] >= b[0]:
            a = (a[0], max(a[1], b[1]))
            merged_ranges.append(a)
        else:
            merged_ranges.append(a)
            merged_ranges.append(b)

    for i in ids:
        for id_range in merged_ranges:
            if id_range[0] <= i <= id_range[1]:
                p1 += 1
                break

    for r in merged_ranges:
        p2 += (r[1] - r[0]) + 1

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
