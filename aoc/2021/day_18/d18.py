from dataclasses import dataclass, field
from itertools import permutations
from typing import Any
from copy import deepcopy

from aoc.cli import file_input


DEBUG = True


@dataclass(order=True)
class Number:
    x: int | Any = None
    y: int | Any = None
    parent: "Number" = field(default=None, compare=False)

    def __repr__(self) -> str:
        return f"[{self.x},{self.y}]"

    def magnitude(self) -> int:
        return 3 * (self.x if isinstance(self.x, int) else self.x.magnitude()) + 2 * (
            self.y if isinstance(self.y, int) else self.y.magnitude()
        )

    def reduce(self) -> "Number":
        new_num = self
        reducing = True
        while reducing:
            old = repr(new_num)
            while explode(new_num):
                if repr(new_num) == old:
                    raise ValueError()
                old = repr(new_num)
            reducing = split(new_num)
            if reducing and repr(new_num) == old:
                raise ValueError()
        return new_num

    def __add__(self, b: "Number") -> "Number":
        print_str = "  " + repr(self) + "\n"
        print_str += "+ " + repr(b) + "\n"
        new_num = Number(self, b)
        self.parent = new_num
        b.parent = new_num
        new_num = new_num.reduce()
        print_str += "= " + repr(new_num) + " -> " + str(new_num.magnitude()) + "\n"
        print(print_str)
        return new_num


def parse(raw_number: str) -> Number | int:
    stack = []
    num = None
    for char in raw_number:
        if char == "[":
            stack.append(Number())
            if len(stack) > 1:
                stack[-1].parent = stack[-2]
        elif char == "]":
            num = stack.pop()
            if stack:
                top = stack[-1]
                if top.x is None:
                    top.x = num
                else:
                    top.y = num
        elif char == ",":
            continue
        else:
            top = stack[-1]
            if top.x is None:
                top.x = int(char)
            else:
                top.y = int(char)
    return num


def explode(num: Number) -> bool:
    def _add_right(num: Number | int, val: int, old_num: Number) -> bool:
        if num is old_num:
            return False
        while isinstance(num, Number) and num.y is old_num:
            old_num = num
            num = num.parent
        if isinstance(num, Number):
            added = _add_right(num.x, val, old_num)
            if added:
                return added
            if isinstance(num.x, int):
                num.x += val
                return True
            elif isinstance(num.y, int):
                num.y += val
                return True
            return _add_right(num.y, val, old_num)
        return False

    def _add_left(nums: list[Number], val: int) -> None:
        for num in reversed(nums):
            if isinstance(num.y, int):
                num.y += val
                return
            elif isinstance(num.x, int):
                num.x += val
                return

    inorder = []

    def _explode(num: Number | int, depth: int) -> bool:
        if isinstance(num, Number):
            exploded = _explode(num.x, depth + 1)
            if exploded:
                return exploded
            if depth > 4:
                if isinstance(num.y, Number):
                    return _explode(num.y, depth + 1)
                _add_right(num.parent, num.y, num)
                _add_left(inorder, num.x)
                if num.parent.x is num:
                    num.parent.x = 0
                else:
                    num.parent.y = 0
                return True
            inorder.append(num)
            return _explode(num.y, depth + 1)
        return False

    return _explode(num, 1)


def split(num: Number) -> bool:
    def _split(num: Number | int) -> bool:
        if isinstance(num, int):
            return False
        is_split = _split(num.x)
        if is_split:
            return is_split
        if isinstance(num.x, int) and num.x > 9:
            val = num.x
            num.x = Number(val // 2, val // 2)
            num.x.parent = num
            if val % 2 == 1:
                num.x.y += 1
            return True
        elif isinstance(num.y, int) and num.y > 9:
            val = num.y
            num.y = Number(val // 2, val // 2)
            num.y.parent = num
            if val % 2 == 1:
                num.y.y += 1
            return True
        return _split(num.y)

    return _split(num)


def main() -> None:
    numbers = []
    with file_input() as file:
        while line := file.readline().strip():
            numbers.append(parse(line))

    round_2_nums = deepcopy(numbers)

    current = numbers[0]
    for number in numbers[1:]:
        current += number
    print(f"part 1: {current.magnitude()}")

    max_mag = 0
    for a, b in permutations(round_2_nums, 2):
        a = deepcopy(a)
        b = deepcopy(b)
        max_mag = max(max_mag, (a + b).magnitude())
    print(f"part 2: {max_mag}")


if __name__ == "__main__":
    main()
