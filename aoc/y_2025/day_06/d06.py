from collections import defaultdict
from operator import add, mul

from aoc.cli import file_input


def main() -> None:
    lines = []
    lines_p2 = []
    with file_input() as file:
        while line := file.readline():
            lines.append(line.split())
            lines_p2.append(line + "     ")

    nums = []
    for line in lines[:-1]:
        nums.append(list(map(int, line)))

    ops_p2 = lines_p2[-1]
    nums_p2 = lines_p2[:-1]

    ops = lines[-1]

    p1 = 0
    p2 = 0

    for col in range(len(nums[0])):
        result = nums[0][col]
        op = add if ops[col] == "+" else mul
        for row in range(1, len(nums)):
            result = op(result, nums[row][col])
        p1 += result

    i = 0
    while i < len(nums_p2[0]):
        if all([r[i] == " " for r in nums_p2]):
            break
        op = add if ops_p2[i] == "+" else mul
        result = 0 if op == add else 1
        while not all([r[i] == " " for r in nums_p2]):
            v_num = 0
            for r in nums_p2:
                if r[i] != " " and r[i] != "\n":
                    v_num *= 10
                    v_num += int(r[i])
            result = op(result, v_num)
            i += 1
        i += 1
        p2 += result

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
