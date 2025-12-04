from aoc.cli import file_input


def count_neighbors(lines: list[list[chr]], i: int, j: int) -> int:
    neighbors = 0

    max_i = len(lines)
    max_j = len(lines[0])

    for i_d in [-1, 0, 1]:
        for j_d in [-1, 0, 1]:
            p_i = i + i_d
            p_j = j + j_d
            if (
                p_i < 0
                or p_j < 0
                or p_i >= max_i
                or p_j >= max_j
                or (i_d == 0 and j_d == 0)
            ):
                continue
            if lines[p_i][p_j] == "@":
                neighbors += 1

    return neighbors


def main() -> None:
    lines = []
    with file_input() as file:
        while line := file.readline().strip():
            lines.append(list(line))
    print(f"{lines}")

    p1 = 0
    p2 = 0

    to_remove = set()
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            cell = lines[i][j]
            if cell != "@":
                continue

            neighbors = count_neighbors(lines, i, j)
            if neighbors < 4:
                p1 += 1
                to_remove.add((i, j))

    while len(to_remove) > 0:
        p2 += len(to_remove)
        for i, j in to_remove:
            lines[i][j] = "."

        to_remove = set()

        for i in range(len(lines)):
            for j in range(len(lines[0])):
                cell = lines[i][j]
                if cell != "@":
                    continue

                neighbors = count_neighbors(lines, i, j)
                if neighbors < 4:
                    to_remove.add((i, j))

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
