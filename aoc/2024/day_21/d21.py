from functools import cache

from aoc.cli import file_input
from aoc.geometry import Point, down, left, right, up

"""
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+

    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
"""
NUMPAD_POINTS = {
    "7": Point(0, 0),
    "8": Point(1, 0),
    "9": Point(2, 0),
    "4": Point(0, 1),
    "5": Point(1, 1),
    "6": Point(2, 1),
    "1": Point(0, 2),
    "2": Point(1, 2),
    "3": Point(2, 2),
    "0": Point(1, 3),
    "A": Point(2, 3),
}
POINT_TO_NUM = {v: k for k, v in NUMPAD_POINTS.items()}
DPAD_POINTS = {
    "^": Point(1, 0),
    "A": Point(2, 0),
    "<": Point(0, 1),
    "v": Point(1, 1),
    ">": Point(2, 1),
}
POINT_TO_DPAD = {v: k for k, v in DPAD_POINTS.items()}


def test(seq: str, depth: int) -> None:
    curr_seq = seq
    print(seq)
    for depth in range(depth, 1, -1):
        next_seq = ""
        p = DPAD_POINTS["A"]
        for c in curr_seq:
            match c:
                case "<":
                    p = left(p)
                case ">":
                    p = right(p)
                case "v":
                    p = up(p)
                case "^":
                    p = down(p)
                case "A":
                    next_seq += POINT_TO_DPAD[p]
            if p not in POINT_TO_DPAD:
                raise ValueError(p)
        print(next_seq)
        curr_seq = next_seq

    final_seq = ""
    p = NUMPAD_POINTS["A"]
    for c in curr_seq:
        match c:
            case "<":
                p = left(p)
            case ">":
                p = right(p)
            case "v":
                p = up(p)
            case "^":
                p = down(p)
            case "A":
                final_seq += POINT_TO_NUM[p]
        if p not in POINT_TO_NUM:
            print("WEE WOO WEE WOO " + curr_seq)
            raise ValueError(p)
    print(final_seq)


@cache
def generate_seq(
    start: Point,
    end: Point,
    num_seq: bool = False,
) -> str:
    diff = start - end
    seq = ""

    if num_seq and start.y == 3 and end.x == 0:
        # UP LEFT -- avoid the void
        seq += "^" * abs(diff.y) + "<" * abs(diff.x)
    elif num_seq and end.y == 3 and start.x == 0:
        # RIGHT DOWN -- avoid the void
        seq += ">" * abs(diff.x) + "v" * abs(diff.y)
    elif not num_seq and start.x == 0 and end.y == 0:
        # RIGHT UP -- avoid the void
        seq += ">" * abs(diff.x) + "^" * abs(diff.y)
    elif not num_seq and end.x == 0 and start.y == 0:
        # DOWN LEFT -- avoid the void
        seq += "v" * abs(diff.y) + "<" * abs(diff.x)
    elif diff.x > 0:
        # LEFT
        if diff.y > 0:
            seq += "<" * diff.x + "^" * diff.y
        else:
            seq += "<" * diff.x + "v" * abs(diff.y)
    else:
        # RIGHT
        if diff.y > 0:
            seq += "^" * diff.y + ">" * abs(diff.x)
        else:
            seq += "v" * abs(diff.y) + ">" * abs(diff.x)
    return seq + "A"


@cache
def get_chunks(code: str) -> tuple[str]:
    chunks = []
    start = 0
    for end, c in enumerate(code):
        if c == "A":
            chunks.append(code[start: end + 1])
            start = end + 1
    return tuple(chunks)


@cache
def find_sequence_by_chunk(
    code: str,
    depth: int = 2,
) -> int:
    if depth == 0:
        return len(code)
    seq_len = 0
    for chunk in get_chunks(code):
        next_chunk = find_sequence(chunk)
        seq_len += find_sequence_by_chunk(next_chunk, depth - 1)
    return seq_len


@cache
def find_sequence(
    code: str,
) -> int:
    robot = DPAD_POINTS["A"]
    seq = ""
    for c in code:
        target_point = DPAD_POINTS[c]
        seq += generate_seq(robot, target_point)
        robot = target_point
    return seq


def find_init_seq(
    code: str,
) -> str:
    seq = ""
    robot = NUMPAD_POINTS["A"]
    for c in code:
        target_point = NUMPAD_POINTS[c]
        seq += generate_seq(robot, target_point, num_seq=True)
        robot = target_point
    return seq


def main() -> None:
    codes = []
    with file_input() as file:
        while line := file.readline().strip():
            codes.append(line)

    p1 = 0
    p2 = 0

    for code in codes:
        seq = find_init_seq(code)

        seq_len_p1 = find_sequence_by_chunk(seq)

        numeric = int(code[:-1])
        p1 += numeric * seq_len_p1

        seq_len_p2 = find_sequence_by_chunk(seq, depth=25)
        p2 += numeric * seq_len_p2

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
