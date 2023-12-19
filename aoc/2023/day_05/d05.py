from itertools import batched

from aoc.cli import file_input
from aoc.geometry import merge_lines, intersection, remove_intersection


def get_next_val(next_val: int, mappings: list[tuple[int, int, int]]) -> int:
    for mapping in mappings:
        if mapping[0] <= next_val < mapping[1]:
            return mapping[2] + next_val - mapping[0]
    return next_val


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
