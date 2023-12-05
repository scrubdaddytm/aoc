from aoc.cli import file_input
from itertools import batched


def get_next_val(next_val: int, mappings: list[tuple[int, int, int]]) -> int:
    for mapping in mappings:
        if mapping[0] <= next_val < mapping[1]:
            return mapping[2] + next_val - mapping[0]
    return next_val


def merge_lines(a: tuple[int, int], b: tuple[int, int]) -> list[tuple[int, int]]:
    if not intersection(a, b):
        return [a, b]
    if a[0] < b[0]:
        return [(a[0], b[1])]
    return [(b[0], a[1])]


def intersection(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int] | None:
    left = max(a[0], b[0])
    right = min(a[1], b[1])
    return None if left > right else (left, right)


def remove_intersection(
    a: tuple[int, int], b: tuple[int, int]
) -> list[tuple[int, int]]:
    if a == b:
        return []
    elif not intersection(a, b):
        return [a]
    elif a[0] <= b[0] and b[1] <= a[1]:  # b within a
        # print(f"B WITHIN A -> {a}, {b}")
        segments = []
        if a[0] <= b[0] - 1:
            segments.append((a[0], b[0] - 1))
        elif b[1] + 1 <= a[1]:
            segments.append((b[1] + 1, a[1]))
        return segments
    elif a[1] == b[0]:
        if a[0] <= a[1] - 1:
            return [(a[0], a[1] - 1)]
        return []
    elif a[0] == b[1]:
        if a[0] + 1 <= a[1]:
            return [(a[0] + 1, a[1])]
        return []
    elif a[0] <= b[0]:  # a before b
        return [(a[0], b[0] - 1)]
    elif a[0] >= b[0]:  # b before a
        return [(b[1] + 1, a[1])]


def main() -> None:
    all_mappings = []
    with file_input() as file:
        seeds = file.readline().strip()
        seeds = list(map(int, seeds.split("seeds: ")[1].split()))
        while line := file.readline():
            if not line.strip():
                continue
            mappings = []
            while map_vals := file.readline().strip():
                raw_mappings = list(map(int, map_vals.split()))
                mappings.append(
                    (
                        raw_mappings[1],
                        raw_mappings[1] + raw_mappings[2],
                        raw_mappings[0],
                    )
                )

            all_mappings.append(sorted(mappings))

    locations = []
    for seed in seeds:
        next_val = seed
        for mappings in all_mappings:
            next_val = get_next_val(next_val, mappings)
        locations.append(next_val)

    print(f"Part 1: {min(locations)}")

    p2_locations = 99999999999999
    for range_start, range_length in batched(seeds, n=2):
        # print(f"SEED: {range_start} to {range_start+range_length-1}")
        lines = [(range_start, range_start + range_length)]
        for idx, mappings in enumerate(all_mappings):
            next_step_lines = []
            for current_line in lines:
                lines_to_check = [current_line]
                while lines_to_check:
                    check_me = lines_to_check.pop()
                    found_overlap = False
                    for l_a, l_b, map_start in mappings:
                        mapping_line = (l_a, l_b)
                        overlap = intersection(check_me, mapping_line)
                        if not overlap:
                            continue
                        found_overlap = True
                        diff = map_start - l_a
                        next_step_lines.append((overlap[0] + diff, overlap[1] + diff))

                        overlap_removed = remove_intersection(check_me, overlap)
                        if overlap_removed:
                            lines_to_check.extend(overlap_removed)
                    if not found_overlap:
                        next_step_lines.extend(overlap_removed)

            if next_step_lines:
                lines = next_step_lines
            lines = sorted(lines)
            merging = [lines[0]]
            for line in lines[1:]:
                merging.extend(merge_lines(merging.pop(), line))
            lines = sorted(merging)

        local_min = min(lines)
        p2_locations = min(local_min[0], p2_locations)

    print(f"Part 2: {p2_locations}")


if __name__ == "__main__":
    main()
