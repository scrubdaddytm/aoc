from aoc.cli import file_input
from aoc.geometry import Point, down, left, right, up
from aoc.print_tools import Color, print_grid

DIRECTIONS = {
    "^": down,
    ">": right,
    "v": up,
    "<": left,
}
BACKWARDS = {
    up: down,
    left: right,
    down: up,
    right: left,
}


def change_color(
    c: str,
    color: Color,
) -> str:
    return color + c + Color.END


def print_warehouse(
    warehouse: dict[Point, str],
    robot: Point,
) -> None:
    print_dict = {}
    for p, c in warehouse.items():
        if c == "#":
            print_dict[p] = change_color(c, Color.BLUE)
        elif c in {"O", "[", "]"}:
            print_dict[p] = change_color(c, Color.PURPLE)
    print_dict[robot] = change_color("@", Color.GREEN)
    print_grid(print_dict)


def simulate(
    warehouse: dict[Point, str],
    robot: Point,
    moves: list[str],
) -> None:
    for move in moves:
        next_point = move(robot)
        cell = warehouse.get(next_point)
        if cell == "#":
            continue
        elif not cell:
            robot = next_point
            continue

        find_room = next_point
        while c := warehouse.get(find_room):
            if c == "#":
                break
            find_room = move(find_room)
        else:
            robot = next_point
            warehouse.pop(next_point)
            warehouse[find_room] = "O"
    print_warehouse(warehouse, robot)


def get_box_points(
    warehouse: dict[Point, str],
    p: Point,
) -> set[Point]:
    box_part = warehouse[p]
    if box_part == "[":
        return set([p, right(p)])
    return set([left(p), p])


def simulate_doubled(
    warehouse: dict[Point, str],
    robot: Point,
    moves: list[str],
) -> None:
    for move in moves:
        next_point = move(robot)
        cell = warehouse.get(next_point)
        if cell == "#":
            continue
        elif not cell:
            robot = next_point
            continue

        find_room = next_point
        if move == left or move == right:
            while c := warehouse.get(find_room):
                if c == "#":
                    break
                find_room = move(find_room)
            else:
                back = BACKWARDS[move]
                walking_back = back(find_room)
                while walking_back != robot:
                    warehouse[find_room] = warehouse[walking_back]
                    find_room = walking_back
                    walking_back = back(walking_back)

                robot = next_point
                warehouse.pop(next_point)
        else:
            current_level = get_box_points(warehouse, next_point)
            points_to_move = []

            while any({warehouse.get(p) for p in current_level}):
                points_to_move.append(current_level)

                next_level = {move(p) for p in current_level}
                if any({warehouse.get(p) == "#" for p in next_level}):
                    break
                box_points = set()
                for p in next_level:
                    if warehouse.get(p) in {"[", "]"}:
                        box_points.update(get_box_points(warehouse, p))
                next_level = box_points
                current_level = next_level
            else:
                for line in reversed(points_to_move):
                    for p in line:
                        if p in warehouse:
                            warehouse[move(p)] = warehouse.get(p)
                            warehouse.pop(p)
                robot = next_point
    print_warehouse(warehouse, robot)


def double(
    warehouse: dict[Point, str],
    robot: Point,
) -> tuple[dict[Point, str], Point]:
    doubled_warehouse = {}
    r = Point(1, 0)
    for p, c in warehouse.items():
        p = Point(p.x * 2, p.y)
        r_p = p.move(r)
        if c == "#":
            doubled_warehouse[p] = "#"
            doubled_warehouse[r_p] = "#"
        else:
            doubled_warehouse[p] = "["
            doubled_warehouse[r_p] = "]"

    doubled_robot = Point(robot.x * 2, robot.y)
    return doubled_warehouse, doubled_robot


def main() -> None:
    warehouse = {}
    moves = []
    robot = None
    with file_input() as file:
        y = 0
        while line := file.readline().strip():
            for x, c in enumerate(line):
                if c == "#" or c == "O":
                    warehouse[Point(x, y)] = c
                elif c == "@":
                    robot = Point(x, y)
            y += 1
        while line := file.readline().strip():
            for d in line:
                moves.append(DIRECTIONS[d])
    print_warehouse(warehouse, robot)
    print(f"{robot=}")

    doubled_warehouse, doubled_robot = double(warehouse, robot)

    simulate(warehouse, robot, moves)

    print_warehouse(doubled_warehouse, doubled_robot)
    simulate_doubled(doubled_warehouse, doubled_robot, moves)

    p1 = 0
    p2 = 0

    for p, c in warehouse.items():
        if c == "O":
            p1 += 100 * p.y + p.x

    for p, c in doubled_warehouse.items():
        if c == "[":
            p2 += 100 * p.y + p.x

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
