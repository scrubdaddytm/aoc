from aoc.cli import file_input
from aoc.geometry import CARDINAL_DIRECTIONS, in_bounds, Point


def main() -> None:
    heights = []
    with file_input() as file:
        while line := file.readline().strip():
            heights.append(list(map(int, list(line))))

    width = len(heights[0])
    length = len(heights)

    risk_level = 0
    low_points = []
    for y in range(length):
        for x in range(width):
            height = heights[y][x]
            is_min = True
            for direction in CARDINAL_DIRECTIONS:
                p = direction(Point(x, y))
                if in_bounds(p, width, length):
                    is_min = is_min and height < heights[p.y][p.x]
            if is_min:
                risk_level += 1 + height
                low_points.append(Point(x, y))

    print(f"part 1: {risk_level=}")

    basins = []
    for low_point in low_points:
        basin = set([low_point])
        dfs = [low_point]
        while dfs:
            p = dfs.pop()
            for direction in CARDINAL_DIRECTIONS:
                next_p = direction(p)
                if (
                    next_p not in basin
                    and in_bounds(next_p, width, length)
                    and heights[next_p.y][next_p.x] < 9
                ):
                    basin.add(next_p)
                    dfs.append(next_p)
        basins.append(basin)

    basins = sorted(basins, key=lambda b: -len(b))

    print(f"part 2: {len(basins[0]) * len(basins[1]) * len(basins[2])}")


if __name__ == "__main__":
    main()
