from aoc.cli import file_input
from dataclasses import dataclass
from enum import Enum
from enum import auto
import pathlib
import numpy


class VarType(Enum):
    OLD = auto()
    STATIC = auto()

@dataclass
class Variable:
    var_type: VarType
    value: int

@dataclass
class Monkey:
    operation: tuple[Variable, str, Variable] = (None, None, None)
    disvisible_test: int = 0
    test_result: dict[bool, int] = None
    items_inspected: int = 0


def display_monkeys(monkeys: list[Monkey]) -> None:
    for idx, monkey in enumerate(monkeys):
        print(f"Monkey {idx}: {monkey.items_inspected}")
    print()


def calculate_worry(item: int, operation: tuple[Variable, str, Variable]) -> int:
    left_operand = item if operation[0].var_type == VarType.OLD else operation[0].value
    right_operand = item if operation[2].var_type == VarType.OLD else operation[2].value
    match operation[1]:
        case "*":
            return int(numpy.multiply(left_operand, right_operand))
        case "+":
            return int(numpy.add(left_operand, right_operand))

    raise ValueError("oops, missed a worry calculation")


def throw_to_monkey(monkey_num: int, item: int):
    path = pathlib.Path(f"./tmp/monkey-{monkey_num}-items")
    if not path.exists():
        path.touch()
    with path.open("a") as items:
        items.write(str(item))
        items.write("\n")


def run_rounds(monkeys: list[Monkey], rounds: int, division_help: int) -> int:
    for r in range(1, rounds+1):
        for idx, monkey in enumerate(monkeys):
            path = pathlib.Path(f"./tmp/monkey-{idx}-items")
            if not path.exists():
                continue
            with path.open() as monkey_items:
                while item := monkey_items.readline().strip():
                    item = calculate_worry(int(item), monkey.operation)

                    if rounds == 20:
                        item //= 3
                    item = int(numpy.remainder(item, division_help))
 
                    new_monkey_num = monkey.test_result[int(numpy.remainder(item, monkey.disvisible_test)) == 0]
                    throw_to_monkey(new_monkey_num, item)

                    monkey.items_inspected += 1
            path.unlink()
        if r % 1000 == 0 or r == 1 or r == 20:
            display_monkeys(monkeys)

    monkey_business = sorted([monkey.items_inspected for monkey in monkeys])
    return monkey_business[-1] * monkey_business[-2]


def define_variable(value: str) -> Variable:
    if value == "old":
        return Variable(VarType.OLD, 0)
    return Variable(VarType.STATIC, int(value))


def parse_monkeys(file) -> list[Monkey]:
    monkeys = []
    current_monkey = None
    division_help = 1
    while line := file.readline():
        if line == "\n":
            continue

        definition = line.strip().split(":")
        attribute = definition[0].split()
        attr_value = definition[1]

        match attribute:
            case ["Monkey", _]:
                current_monkey = Monkey()
                current_monkey.test_result = {}
                monkeys.append(current_monkey)
                path = pathlib.Path(f"./tmp/monkey-{len(monkeys)-1}-items")
                if path.exists():
                    path.unlink()
            case ["Starting", "items"]:
                for item in list(map(int, attr_value.split(','))):
                    throw_to_monkey(len(monkeys)-1, item)
            case ["Operation"]:
                operation_def = attr_value.split()
                current_monkey.operation = (
                    define_variable(operation_def[2]),
                    operation_def[3].strip(),
                    define_variable(operation_def[4]),
                )
            case ["Test"]:
                test_def = attr_value.split()
                div_test = int(test_def[2])
                current_monkey.disvisible_test = div_test
                division_help *= div_test
            case ["If", "true"]:
                test_result = attr_value.split()
                current_monkey.test_result[True] = int(test_result[3])
            case ["If", "false"]:
                test_result = attr_value.split()
                current_monkey.test_result[False] = int(test_result[3])
            case _:
                continue
    return monkeys, division_help


def main() -> None:
    for rounds in [20, 10_000]:
        monkeys = []
        division_help = 1
        with file_input() as file:
            monkeys, division_help = parse_monkeys(file)

        for monkey in monkeys:
            print(f"{monkey}")
        print(f"{division_help=}")
        monkey_business = run_rounds(monkeys, rounds, division_help)
        display_monkeys(monkeys)
        print(f"{rounds} rounds of {monkey_business=}")


if __name__ == "__main__":
    main()
