from aoc.cli import file_input
from dataclasses import dataclass
import string
import re


@dataclass(frozen=True, order=True)
class Cell:
    r: int
    c: int

    def __repr__(self) -> str:
        return f"({self.r}, {self.c})"


def left(cell: Cell) -> Cell:
    return Cell(cell.r, cell.c - 1)


def right(cell: Cell) -> Cell:
    return Cell(cell.r, cell.c + 1)


def up(cell: Cell) -> Cell:
    return Cell(cell.r - 1, cell.c)


def down(cell: Cell) -> Cell:
    return Cell(cell.r + 1, cell.c)


TURN = {
    left: {"L": down, "R": up},
    right: {"L": up, "R": down},
    up: {"L": left, "R": right},
    down: {"L": right, "R": left},
}

DIR = {
    left: "<",
    right: ">",
    up: "^",
    down: "v",
}

DIR_VAL = {
    right: 0,
    down: 1,
    left: 2,
    up: 3,
}


def print_graph(
    row_bounds: dict[int, dict[str, int]],
    col_bounds: dict[int, dict[str, int]],
    walls: set[Cell],
    path: dict[int, dict[int, str]] | None = None,
) -> None:
    if not path:
        path = {}
    for r, rb in sorted(row_bounds.items()):
        print_val = " " * rb["l"]
        for c in range(rb["l"], rb["r"] + 1):
            cell = Cell(r, c)
            if cell in walls:
                print_val += "#"
            elif path.get(r, {}).get(c):
                print_val += path[r][c]
            else:
                print_val += "."
        print(print_val)
    print()


def loop_traversal(
    row_bounds: dict[int, dict[str, int]],
    col_bounds: dict[int, dict[str, int]],
    curr: Cell,
    direction: callable,
) -> Cell:
    next_cell = direction(curr)
    if direction in {left, right}:
        left_bound = row_bounds[next_cell.r]["l"]
        right_bound = row_bounds[next_cell.r]["r"]

        if left_bound > next_cell.c:
            next_cell = Cell(next_cell.r, right_bound)
        if right_bound < next_cell.c:
            next_cell = Cell(next_cell.r, left_bound)
    else:
        down_bound = col_bounds[next_cell.c]["d"]
        up_bound = col_bounds[next_cell.c]["u"]

        if down_bound > next_cell.r:
            next_cell = Cell(up_bound, next_cell.c)
        elif up_bound < next_cell.r:
            next_cell = Cell(down_bound, next_cell.c)
    return next_cell


def calculate_cube_edge_pairs(
    row_bounds: dict[int, dict[str, int]], col_bounds: dict[int, dict[str, int]], cube_face_size: int
) -> dict[int, tuple[int, int]]:
    seen_edges = set()

    for row in range(1, 4 * cube_face_size, cube_face_size):
        row_bound = row_bounds.get(row)
        if not row_bound:
            continue
        for col in range(1, 4 * cube_face_size, cube_face_size):
            col_bound = col_bounds.get(col)
            if col_bound and col_bound["d"] <= row <= col_bound["u"] and row_bound["l"] <= col <= row_bound["r"]:
                unseen_edge_points = (
                    set(
                        [
                            Cell(row, col),
                            Cell(row + cube_face_size - 1, col),
                            Cell(row, col + cube_face_size - 1),
                            Cell(row + cube_face_size - 1, col + cube_face_size - 1),
                        ]
                    )
                    - seen_edges
                )

                seen_edges |= unseen_edge_points

    for edge in sorted(seen_edges):
        print(f"{edge}")
    print(f"total edges checked: {len(seen_edges)}")


def cube_traversal(
    row_bounds: dict[int, dict[str, int]],
    col_bounds: dict[int, dict[str, int]],
    curr: Cell,
    direction: callable,
    cube_face_size: int,
) -> tuple[Cell, callable]:
    # YES I AM SHAMEFULLY HARDCODING THIS :(
    if cube_face_size == 4:
        pass
    if cube_face_size == 50:
        if curr.r == 1 and 51 <= curr.c <= 100 and direction == up:
            # 1 -> 6 GOOD
            return Cell(curr.c + 100, 1), right
        elif curr.c == 1 and 151 <= curr.r <= 200 and direction == left:
            # 6 -> 1 GOOD
            return Cell(1, curr.r - 100), down
        elif curr.r == 1 and 101 <= curr.c <= 150 and direction == up:
            # 2 -> 6 GOOD
            return Cell(200, curr.c - 100), up
        elif curr.r == 200 and 1 <= curr.c <= 50 and direction == down:
            # 6 -> 2 GOOD
            return Cell(1, curr.c + 100), down
        elif curr.r == 50 and 101 <= curr.c <= 150 and direction == down:
            # 2 -> 3 GOOD
            return Cell(curr.c - 50, 100), left
        elif curr.c == 100 and 51 <= curr.r <= 100 and direction == right:
            # 3 -> 2 GOOD
            return Cell(50, curr.r + 50), up
        elif curr.r == 101 and 1 <= curr.c <= 50 and direction == up:
            # 4 -> 3 GOOD
            return Cell(curr.c + 50, 51), right
        elif curr.c == 51 and 51 <= curr.r <= 100 and direction == left:
            # 3 -> 4 GOOD 
            return Cell(101, curr.r - 50), down
        elif curr.r == 150 and 51 <= curr.c <= 100 and direction == down:
            # 5 -> 6 GOOD
            return Cell(100 + curr.c, 50), left
        elif curr.c == 50 and 151 <= curr.r <= 200 and direction == right:
            # 6 -> 5 GOOD
            return Cell(150, curr.r - 100), up
        elif curr.c == 51 and 1 <= curr.r <= 50 and direction == left:
            # 1 -> 4 GOOD
            return Cell(101 + abs(curr.r - 50), 1), right
        elif curr.c == 1 and 101 <= curr.r <= 150 and direction == left:
            # 4 -> 1 GOOD
            return Cell(1 + abs(curr.r - 150), 51), right
        elif curr.c == 150 and 1 <= curr.r <= 50 and direction == right:
            # 2 -> 5 GOOD
            return Cell(101 + abs(curr.r - 50), 100), left
        elif curr.c == 100 and 101 <= curr.r <= 150 and direction == right:
            # 5 -> 2 GOOD
            return Cell(1 + abs(curr.r - 150), 150), left

    return direction(curr), direction


def traverse(
    row_bounds: dict[int, dict[str, int]],
    col_bounds: dict[int, dict[str, int]],
    walls: set[Cell],
    instructions: str,
    cube_face_size: int | None = None,
) -> tuple[Cell, int]:

    curr = Cell(1, row_bounds[1]["l"])
    print(f"STARTING AT : {curr}")
    path = {}

    direction = right
    for inst in re.findall(r"(\d+|L|R)", instructions):
        if inst == "R" or inst == "L":
            direction = TURN[direction][inst]
            continue
        distance = int(inst)
        for _ in range(distance):
            path.setdefault(curr.r, {})[curr.c] = DIR[direction]

            new_direction = None
            if cube_face_size:
                next_cell, new_direction = cube_traversal(row_bounds, col_bounds, curr, direction, cube_face_size)
                print(f"{next_cell=}, {direction.__name__}")
            else:
                next_cell = loop_traversal(row_bounds, col_bounds, curr, direction)

            if next_cell in walls:
                break
            if next_cell.r < 1 or next_cell.r > 200 or next_cell.c < 1 or next_cell.c > 150:
                raise ValueError(next_cell)
            # print_graph(row_bounds, col_bounds, walls, path)
            # print(f"{curr} {DIR[direction]} {next_cell}")
            if new_direction:
                direction = new_direction
            curr = next_cell

    print_graph(row_bounds, col_bounds, walls, path)

    return curr, DIR_VAL[direction]


def main() -> None:
    row_bounds = {}
    col_bounds = {}
    walls = set()
    instructions = None
    cube_face_size = 0

    with file_input() as file:
        row_idx = 1
        print(file.name)
        cube_face_size = 50 if "d22.in" in file.name else 4
        while row := file.readline():
            if row == "\n":
                break
            col_idx = 1
            while row[col_idx - 1] in string.whitespace:
                col_idx += 1
            left_col = col_idx
            while col_idx < len(row) and row[col_idx - 1] != " ":
                c_b = col_bounds.setdefault(col_idx, {})
                c_b["u"] = max(c_b.get("u", 1), row_idx)
                c_b["d"] = min(c_b.get("d", 6969696969), row_idx)
                col_bounds[col_idx] = c_b

                if row[col_idx - 1] == "#":
                    walls.add(Cell(row_idx, col_idx))
                col_idx += 1
            row_bounds[row_idx] = {"l": left_col, "r": col_idx - 1}

            row_idx += 1
        instructions = file.readline().strip()

    print("row_bounds")
    for k, v in sorted(row_bounds.items()):
        print(f"{k}: {v}")
    print("col_bounds")
    for k, v in sorted(col_bounds.items()):
        print(f"{k}: {v}")

    print_graph(row_bounds, col_bounds, walls)
    final_cell, dir_val = traverse(row_bounds, col_bounds, walls, instructions)
    print(f"Part 1: {final_cell}, result: {(1000 * final_cell.r) + (4 * final_cell.c) + dir_val}")

    calculate_cube_edge_pairs(row_bounds, col_bounds, cube_face_size)

    final_cell, dir_val = traverse(row_bounds, col_bounds, walls, instructions, cube_face_size)
    print(f"Part 1: {final_cell}, result: {(1000 * final_cell.r) + (4 * final_cell.c) + dir_val}")


if __name__ == "__main__":
    main()
