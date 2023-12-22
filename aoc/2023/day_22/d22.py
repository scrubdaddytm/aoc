from collections import defaultdict
from aoc.cli import file_input
from aoc.geometry import Point3D


DOWN = Point3D(0, 0, -1)
UP = Point3D(0, 0, 1)


def update(grid: list[list[list[str]]], a: Point3D, b: Point3D, brick: str = "#") -> None:
    for x in range(a.x, b.x + 1):
        for y in range(a.y, b.y + 1):
            for z in range(a.z, b.z + 1):
                grid[x][y][z] = brick


def overlap(grid, a, b, piece: chr = ".") -> set[chr]:
    overlappers = set()
    for x in range(a.x, b.x + 1):
        for y in range(a.y, b.y + 1):
            for z in range(a.z, b.z + 1):
                if grid[x][y][z] != piece and grid[x][y][z] != ".":
                    overlappers.add(grid[x][y][z])
    return overlappers


def entry_key(entry: tuple[tuple[Point3D, Point3D], int]) -> int:
    return (10**6 + entry[0][0].z) + (10**4 + entry[0][0].y) + (10**2 + entry[0][0].x)


def print_x(grid):
    print("  x")
    for z in reversed(range(1, len(grid[0][0]))):
        row = ""
        for x in range(len(grid)):
            seen = set()
            for y in range(len(grid[0])):
                if grid[x][y][z] != ".":
                    seen.add(grid[x][y][z])
            if not seen:
                row += "."
            elif len(seen) == 1:
                row += chr(list(seen)[0])
            else:
                row += "?"
        print(row + f" {z}")
    print("-" * 10)


def print_y(grid):
    print("  y")
    for z in reversed(range(1, len(grid[0][0]))):
        row = ""
        for y in range(len(grid[0])):
            seen = set()
            for x in range(len(grid)):
                if grid[x][y][z] != ".":
                    seen.add(grid[x][y][z])
            if not seen:
                row += "."
            elif len(seen) == 1:
                row += chr(list(seen)[0])
            else:
                row += "?"
        print(row + f" {z}")
    print("-" * 10)


def main() -> None:
    pieces = []
    grid = [[["." for _ in range(350)] for _ in range(10)] for _ in range(10)]
    with file_input() as file:
        piece = ord("A")
        while line := file.readline().strip():
            a, b = line.split("~")
            a = Point3D(*list(map(int, a.split(","))))
            b = Point3D(*list(map(int, b.split(","))))
            pieces.append(((a, b), piece))
            for x in range(a.x, b.x + 1):
                for y in range(a.y, b.y + 1):
                    for z in range(a.z, b.z + 1):
                        grid[x][y][z] = piece
            piece += 1

    pieces = sorted(pieces, key=entry_key)

    # print_x(grid)
    # print_y(grid)

    moved = True
    while moved:
        moved = False
        updated_pieces = []
        for (a, b), piece in pieces:
            # print(f"{chr(piece)} -> {a}, {b}")
            if a.z == 1 or b.z == 1:
                updated_pieces.append(((a, b), piece))
                continue
            update(grid, a, b, ".")
            a_0 = a
            b_0 = b
            a_1 = a.move(DOWN)
            b_1 = b.move(DOWN)
            while not overlap(grid, a_1, b_1) and a_1.z > 0 and b_1.z > 0:
                a_0 = a_1
                b_0 = b_1
                a_1 = a_1.move(DOWN)
                b_1 = b_1.move(DOWN)
            update(grid, a_0, b_0, piece)
            if a != a_0:
                moved = True
            updated_pieces.append(((a_0, b_0), piece))
        pieces = updated_pieces
    # print_x(grid)
    # print_y(grid)

    supported = defaultdict(set)
    supporting = defaultdict(set)
    for (a, b), piece in pieces:
        a_1 = a.move(UP)
        b_1 = b.move(UP)
        overlappers = overlap(grid, a_1, b_1, piece)
        supporting[piece] = overlappers
        for p in overlappers:
            supported[p].add(piece)

    disintegratable = set()
    for _, piece in pieces:
        possible = True
        for other in supporting[piece]:
            if len(supported[other]) <= 1:
                possible = False
                break
        if possible:
            disintegratable.add(piece)
    # print(f"Disintegratable: {list(map(chr, disintegratable))}")
    print(f"Part 1: {len(disintegratable)}")

    total = 0
    for _, piece in pieces:
        if piece in disintegratable:
            continue
        fell = set()
        fell.add(piece)
        q = [piece]
        while q:
            curr = q.pop(0)
            for other in supporting[curr]:
                if supported[other] <= fell:
                    fell.add(other)
                    q.append(other)
        print(f"{chr(piece)} -> {list(map(chr, fell))}")
        total += len(fell) - 1

    print(f"Part 2: {total}")


if __name__ == "__main__":
    main()
