from aoc.cli import file_input


def process_tasks(tasks: list[str]) -> tuple[int, list[list[str]]]:
    strength = 0
    render = [["." for _ in range(40)] for __ in range(6)]
    X = 1
    cycle = 1
    for task in tasks:
        op = task[0]

        task_cost = 1
        if op == "addx":
            task_cost = 2

        for _ in range(task_cost):
            if (cycle - 20) % 40 == 0:
                strength += (cycle * X)
                print(f"{cycle=} * {X=} + {strength=}")

            v_pos = (cycle-1) // 40
            h_pos = (cycle - 1) % 40
            render[v_pos][h_pos] = "#" if X-1 <= h_pos <= X+1 else "."
            cycle += 1

        if op == "addx":
            X += int(task[1])
    return strength, render


def main() -> None:
    tasks = []
    with file_input() as file:
        while line := file.readline().strip().split():
            tasks.append(line)

    sum_of_strength, render = process_tasks(tasks)
    print(f"{sum_of_strength=}")
    for line in render:
        print("".join(line))

if __name__ == "__main__":
    main()
