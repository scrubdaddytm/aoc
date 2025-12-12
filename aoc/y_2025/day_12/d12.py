from functools import cache

from aoc.cli import file_input
from aoc.geometry import Point
from aoc.print_tools import print_point_grid


@cache
def rotate_90(shape: frozenset[Point]) -> frozenset[Point]:
    transposed = set()
    for p in shape:
        transposed.add(Point(p.y, p.x))

    new_shape = set()
    for p in transposed:
        new_shape.add(Point(2 - p.x, p.y))

    return frozenset(new_shape)


@cache
def mirror(shape: frozenset[Point]) -> frozenset[Point]:
    new_shape = set()
    for p in shape:
        new_shape.add(Point(p.x, 2 - p.y))

    return frozenset(new_shape)


@cache
def move(shape: frozenset[Point], p: Point) -> frozenset[Point]:
    new_shape = set()
    for old_point in shape:
        new_shape.add(old_point.move(p))

    return frozenset(new_shape)


def bt(region, placements, requirements, present_variations) -> bool:
    print_point_grid(placements)
    print()
    if sum(requirements) == 0:
        print_point_grid(placements)
        return True

    for delta_p in region:
        for i in range(len(requirements)):
            if requirements[i] == 0:
                continue

            for pv_idx, pv in enumerate(present_variations[i]):
                # key = (delta_p, i, pv_idx)
                place_me = move(pv, delta_p)
                if place_me <= region and not placements & place_me:
                    placements |= place_me
                    requirements[i] -= 1
                    if bt(region, placements, requirements, present_variations):
                        return True
                    placements -= place_me
                    requirements[i] += 1

    return False


def pack(region_dims, requirements, present_variations) -> bool:
    region = set()
    for x in range(region_dims[0]):
        for y in range(region_dims[1]):
            region.add(Point(x, y))
    print_point_grid(region)

    placements = set()
    return bt(region, placements, requirements, present_variations)


def main() -> None:
    presents = []
    regions = []
    with file_input() as file:
        for _ in range(6):
            i = 0
            shape = set()
            file.readline()
            while line := file.readline().strip():
                for j, c in enumerate(line):
                    if c == "#":
                        shape.add(Point(j, i))
                i += 1
            presents.append(frozenset(shape))

        while line := file.readline().strip():
            region, counts = line.split(": ")
            region = tuple(map(int, region.split("x")))
            counts = list(map(int, counts.split(" ")))

            regions.append((region, counts))

    # present_variations = []
    # for i, present in enumerate(presents):
    #     variations = set()
    #     present_variations.append(variations)

    #     variations.add(present)
    #     for j in range(4):
    #         present = rotate_90(present)
    #         variations.add(present)

    #     variations.add(mirror(present))
    #     for j in range(4):
    #         present = rotate_90(present)
    #         variations.add(mirror(present))

    p1 = 0
    p2 = 0

    for region, requirements in regions:
        print(f"{region=} -> {requirements=}")
        print(
            f"area={region[0] * region[1]} ?>= {sum(a * b for a, b in zip(requirements, [len(pv) for pv in presents]))}"
        )
        if (
            sum(a * b for a, b in zip(requirements,
                [len(pv) for pv in presents]))
            <= region[0] * region[1]
        ):
            p1 += 1
        # if pack(region, requirements, present_variations):
        # p1 += 1

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
