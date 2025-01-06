from aoc.cli import file_input
from math import lcm


def find_count(instructions: str, graph: dict[str,[str,str]], start: str = "AAA", p2: bool = False) -> int:
    end = "ZZZ"
    count = 0
    while start != end:
        if p2 and start[-1] == "Z":
            break
        char = instructions[count % len(instructions)]
        if char == "L":
            start = graph[start][0]
        else:
            start = graph[start][1]
        count += 1
    return count


def main() -> None:
    graph = {}
    instructions = None
    with file_input() as file:
        instructions = file.readline().strip()
        file.readline()
        while line := file.readline():
            k, v = line.split(" = ")
            l, r = v[1:-2].split(", ")
            graph[k] = (l, r)
    print(graph)
    print(f"Part 1: {find_count(instructions, graph)}")

    all_end_with_a = []
    for key in graph.keys():
        if key[-1] == "A":
            all_end_with_a.append(find_count(instructions, graph, key, True))

    print(f"Part 2: {lcm(*all_end_with_a)}")


if __name__ == "__main__":
    main()
