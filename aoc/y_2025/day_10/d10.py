from collections import defaultdict, deque

import z3
from aoc.cli import file_input


def buttonmash(target, buttons) -> int:
    seen = set()
    state = frozenset()
    presses = tuple(0 for _ in buttons)
    q = deque([(state, presses)])
    while q:
        state, presses = q.popleft()

        press_count = sum(presses) + 1
        for i, b in enumerate(buttons):
            next_state = state ^ b
            if next_state == target:
                return press_count

            if next_state in seen:
                continue

            seen.add(next_state)
            new_presses = list(presses)
            new_presses[i] += 1
            q.append((next_state, tuple(new_presses)))

    return -1


def alright(joltage, buttons) -> int:
    solver = z3.Optimize()

    button_vars = [z3.Int(chr(i + ord("a"))) for i in range(len(buttons))]
    for b in button_vars:
        solver.add(b >= 0)
    joltage_buttons = defaultdict(list)

    for i, b in enumerate(buttons):
        for j in b:
            joltage_buttons[j].append(i)

    for i, jb in joltage_buttons.items():
        solver.add(joltage[i] == sum([button_vars[j] for j in jb]))

    minim = 0
    for b in button_vars:
        minim += b
    solver.minimize(minim)
    solver.check()
    model = solver.model()

    result = sum([model.evaluate(b).as_long() for b in button_vars])
    return result


def main() -> None:
    machines = []
    with file_input() as file:
        while line := file.readline().strip():
            split_machine = line.split(" ")

            target = set()
            for i, c in enumerate(split_machine[0][1:-1]):
                if c == "#":
                    target.add(i)

            buttons = []
            for b in split_machine[1:-1]:
                buttons.append(frozenset(map(int, b[1:-1].split(","))))

            buttons = sorted(buttons, key=lambda x: len(x))

            joltage = tuple(map(int, split_machine[-1][1:-1].split(",")))

            machines.append(
                (
                    frozenset(target),
                    tuple(buttons),
                    joltage,
                )
            )

    p1 = 0
    p2 = 0

    for target, buttons, joltage in machines:
        p1 += buttonmash(target, buttons)
        p2 += alright(joltage, buttons)

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
