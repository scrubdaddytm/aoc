from aoc.cli import file_input
from dataclasses import dataclass


P1_POINTS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

P2_POINTS = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


PAIRS = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<",
}


REV_PAIRS = {val: key for key, val in PAIRS.items()}


def main() -> None:
    lines = []
    with file_input() as file:
        while line := file.readline().strip():
            lines.append(line)

    bad_chars = []
    incomplete_stacks = []
    for line in lines:
        stack = []
        bad = False
        for char in line:
            if char in PAIRS and stack[-1] != PAIRS[char]:
                bad_chars.append(char)
                bad = True
                break
            elif char in PAIRS:
                stack.pop()
            else:
                stack.append(char)
        if stack and not bad:
            incomplete_stacks.append(stack)

    print(f"part 1: {sum([P1_POINTS[char] for char in bad_chars])}")

    completion_points = []
    for line in incomplete_stacks:
        points = 0
        for char in reversed(line):
            points *= 5
            points += P2_POINTS[REV_PAIRS[char]]
        completion_points.append(points)

    completion_points = sorted(completion_points)
    print(f"part 2: {completion_points[(len(completion_points)//2)]}")


if __name__ == "__main__":
    main()
