from aoc.cli import file_input
from itertools import product


def is_possible(test_val: int, nums: list[int], ops: str):
    for ops in product(ops, repeat=len(nums) - 1):
        result = nums[0]
        for op, num in zip(ops, nums[1:]):
            if result > test_val:
                break
            if op == "*":
                result *= num
            elif op == "+":
                result += num
            else:
                result = int(f"{result}{num}")
        if result == test_val:
            return "".join(ops)
    return None


def main() -> None:
    equations = []
    with file_input() as file:
        while line := file.readline().strip():
            test_value, nums = line.split(": ")
            equations.append((int(test_value), list(map(int, nums.split()))))

    p1 = 0
    p2 = 0

    for test_value, nums in equations:
        if ops := is_possible(test_value, nums, "+*"):
            p1 += test_value

        if ops := is_possible(test_value, nums, "+*c"):
            p2 += test_value

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
