from aoc.cli import file_input
from dataclasses import dataclass
from collections import deque
import re


@dataclass(frozen=True)
class Expression:
    monkey_1: str
    operator: str
    monkey_2: str


@dataclass(frozen=True)
class Monkey:
    val: int | None = None
    expr: Expression | None = None


def find_humn_path(monkeys: dict[str, Monkey]) -> list[str]:
    q = deque()
    q.append("root")
    prev = {}
    seen = set()

    while q:
        monkey_name = q.popleft()
        if monkey_name in seen:
            continue
        if monkey_name == "humn":
            break
        seen.add(monkey_name)
        if monkeys[monkey_name].expr:
            l = monkeys[monkey_name].expr.monkey_1
            r = monkeys[monkey_name].expr.monkey_2
            prev[l] = monkey_name
            prev[r] = monkey_name
            q.append(l)
            q.append(r)
    path = set()
    m = "humn"
    while m != "root":
        path.add(m)
        m = prev[m]
    return set(path)


def calculate(monkeys: dict[str, Monkey], path: set[str] | None = None) -> int:
    memoize = {}
    def recurse(monkey_name: str, target: int | None = None) -> int:
        if monkey_name == "humn" and path:
            print(f"HUMN: {target}")
            return target

        if memoize.get(monkey_name):
            return memoize[monkey_name]

        monkey = monkeys[monkey_name]
        if monkey.val:
            return monkey.val

        m1 = monkey.expr.monkey_1
        m2 = monkey.expr.monkey_2

        if path and m1 in path and m2 in path:
            raise ValueError("hm, two paths with humn")

        result = None
        if path and (m1 in path or m2 in path):
            match [monkey.expr.operator, m1 in path]:
                case ["-", True]:
                    # l = target + r
                    r_operand = recurse(m2)
                    result = recurse(m1, target+r_operand)
                case ["-", False]:
                    # r = l - target
                    l_operand = recurse(m1)
                    result = recurse(m2, l_operand-target)
                case ["+", True]:
                    r_operand = recurse(m2)
                    result = recurse(m1, target-r_operand)
                case ["+", False]:
                    # r = target - l
                    l_operand = recurse(m1)
                    result = recurse(m2, target-l_operand)
                case ["/", True]:
                    # l = target * r
                    r_operand = recurse(m2)
                    result = recurse(m1, target*r_operand)
                case ["/", False]:
                    # r = l // target
                    l_operand = recurse(m1)
                    result = recurse(m2, l_operand//target)
                case ["*", True]:
                    # l = target // r
                    r_operand = recurse(m2)
                    result = recurse(m1, target//r_operand)
                case ["*", False]:
                    # r = targetr // l
                    l_operand = recurse(m1)
                    result = recurse(m2, target//l_operand)
                case _:
                    print("NO DICE")
        else:
            l_operand = recurse(m1)
            r_operand = recurse(m2)
            match monkey.expr.operator:
                case "-":
                    result = l_operand - r_operand
                case "+":
                    result = l_operand + r_operand
                case "/":
                    result = l_operand // r_operand
                case "*":
                    result = l_operand * r_operand

        memoize[monkey_name] = result
        return result
    if path:
        l = monkeys["root"].expr.monkey_1
        r = monkeys["root"].expr.monkey_2
        if l in path and r in path:
            raise ValueError('whoops both ways?')
        elif l in path:
            r_operand = recurse(r)
            return recurse(l, r_operand)
        else:
            l_operand = recurse(l)
            return recurse(r, l_operand)
    else:
        return recurse("root")


def main() -> None:
    monkeys = {}
    with file_input() as file:
        while line := file.readline():
            spl = line.split(':')
            try:
                val = int(spl[1])
                monkeys[spl[0]] = Monkey(val=val)
            except ValueError:
                raw_expr = spl[1].split()
                monkeys[spl[0]] = Monkey(expr=Expression(raw_expr[0], raw_expr[1], raw_expr[2]))
    print(f"Part 1: {calculate(monkeys)}")

    path = find_humn_path(monkeys)
    print(f"Part 2: {calculate(monkeys, path)}")



if __name__ == "__main__":
    main()
