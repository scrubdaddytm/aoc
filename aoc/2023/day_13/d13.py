from aoc.cli import file_input


def find_mirrors(patterns: list[list[str]]) -> tuple[list[int], list[int]]:
    vertical_mirrors = []
    horizontal_mirrors = []
    for pattern in patterns:
        mirrored = True
        for y in range(1, len(pattern)):
            mirrored = True
            t_idx = b_idx = 0
            mid_val = len(pattern) // 2
            if y < mid_val:
                t_idx = 0
                b_idx = 2 * y
            else:
                t_idx = max(0, y - abs(len(pattern) - y))
                b_idx = min(y + mid_val, len(pattern))

            for x in range(len(pattern[0])):
                top = [row[x] for row in pattern[t_idx:y]]
                bottom = list(reversed([row[x] for row in pattern[y:b_idx]]))
                if top != bottom:
                    mirrored = False
                    break
            if mirrored:
                horizontal_mirrors.append(y)
                break
        if not mirrored:
            mirrored = True
            for x in range(1, len(pattern[0])):
                mirrored = True
                l_idx = r_idx = 0
                mid_val = len(pattern[0]) // 2
                if x < mid_val:
                    l_idx = 0
                    r_idx = 2 * x
                else:
                    l_idx = max(0, x - abs(x - len(pattern[0])))
                    r_idx = min(x + mid_val, len(pattern[0]))

                for y, row in enumerate(pattern):
                    left = list(row[l_idx:x])
                    right = list(reversed(row[x:r_idx]))
                    if left != right:
                        mirrored = False
                        break
                if mirrored:
                    vertical_mirrors.append(x)
                    break
    return vertical_mirrors, horizontal_mirrors


def find_diff(pattern: list[str]) -> tuple[int, int]:
    diff_count = 0
    for y in range(1, len(pattern)):
        t_idx = b_idx = 0
        mid_val = len(pattern) // 2
        if y < mid_val:
            t_idx = 0
            b_idx = 2 * y
        else:
            t_idx = max(0, y - abs(len(pattern) - y))
            b_idx = min(y + mid_val, len(pattern))

        diff_count = 0
        for x in range(len(pattern[0])):
            top = [row[x] for row in pattern[t_idx:y]]
            bottom = list(reversed([row[x] for row in pattern[y:b_idx]]))
            for idx in range(len(top)):
                if top[idx] != bottom[idx]:
                    diff_count += 1
        if diff_count == 1:
            return (0, y)

    for x in range(1, len(pattern[0])):
        l_idx = r_idx = 0
        mid_val = len(pattern[0]) // 2
        if x < mid_val:
            l_idx = 0
            r_idx = 2 * x
        else:
            l_idx = max(0, x - abs(x - len(pattern[0])))
            r_idx = min(x + mid_val, len(pattern[0]))

        diff_count = 0
        for y, row in enumerate(pattern):
            left = list(row[l_idx:x])
            right = list(reversed(row[x:r_idx]))
            for idx in range(len(left)):
                if left[idx] != right[idx]:
                    diff_count += 1
        if diff_count == 1:
            return (x, 0)


def main() -> None:
    patterns = []
    with file_input() as file:
        pattern = []
        while line := file.readline():
            line = line.strip()
            if line == "":
                patterns.append(pattern)
                pattern = []
            else:
                pattern.append(line.strip())
        patterns.append(pattern)

    vertical_mirrors, horizontal_mirrors = find_mirrors(patterns)
    print(f"Part 1: {sum(vertical_mirrors) + 100*sum(horizontal_mirrors)}")
    print(f"{vertical_mirrors}, {horizontal_mirrors}")

    new_vert = []
    new_hori = []
    for pattern in patterns:
        diff = find_diff(pattern)
        new_vert.append(diff[0])
        new_hori.append(diff[1])

    print(f"{new_vert}, {new_hori}")
    print(f"Part 2: {sum(new_vert) + 100*sum(new_hori)}")


if __name__ == "__main__":
    main()
