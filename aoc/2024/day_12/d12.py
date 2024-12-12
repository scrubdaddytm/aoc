from collections import defaultdict, deque

from aoc.cli import file_input
from aoc.geometry import CARDINAL_DIRECTIONS, Point, down, left, right, up

RIGHT = {
    up: right,
    right: down,
    down: left,
    left: up,
}


def group_plots(plots: dict[Point, str]) -> dict[str, list[tuple[set[Point], int]]]:
    grouped_plots = defaultdict(list)

    seen = set()
    for root_point, c in plots.items():
        if root_point in seen:
            continue

        plot = set()
        plot.add(root_point)
        perimeter = 0
        per_set = set()

        q = deque()
        q.append(root_point)
        seen.add(root_point)
        while q:
            p = q.popleft()

            for d in CARDINAL_DIRECTIONS:
                next_point = d(p)
                neighbor = plots.get(next_point)
                if neighbor and neighbor == c:
                    plot.add(next_point)
                    if next_point not in seen:
                        seen.add(next_point)
                        q.append(next_point)
                else:
                    perimeter += 1
                    per_set.add(next_point)

        grouped_plots[c].append((plot, perimeter, per_set))

    return grouped_plots


def count_sides(plot: set[Point]) -> int:
    side_count = 0

    for p in plot:
        for d in CARDINAL_DIRECTIONS:
            r_d = RIGHT[d]
            maybe_corner = set([d(p), r_d(p)])
            intersection = maybe_corner & plot
            if not intersection:
                side_count += 1
            elif len(intersection) == 2 and d(r_d(p)) not in plot:
                side_count += 1

    return side_count


def main() -> None:
    plots = {}
    with file_input() as file:
        i = 0
        while line := file.readline().strip():
            for j, plant in enumerate(line):
                plots[Point(j, i)] = plant
            i += 1

    grouped_plots = group_plots(plots)

    p1 = 0
    p2 = 0
    for c, regions in grouped_plots.items():
        for plot, perimeter_size, perimeter in regions:
            area = len(plot)
            sides = count_sides(plot)
            p1 += area * perimeter_size
            p2 += area * sides

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
