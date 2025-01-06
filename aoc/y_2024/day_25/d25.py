from itertools import product

from aoc.cli import file_input


def main() -> None:
    locks = []
    keys = []
    with file_input() as file:
        while line := file.readline():
            obj = [line.strip()]
            while next_line := file.readline().strip():
                obj.append(next_line)

            if all(c == "#" for c in obj[0]):
                locks.append(obj[1:])
            else:
                keys.append(obj[:-1])

    height_based_locks = []
    for lock in locks:
        height_lock = [0 for _ in range(5)]
        for line in lock:
            for i, c in enumerate(line):
                if c == "#":
                    height_lock[i] += 1
        height_based_locks.append(height_lock)

    height_based_keys = []
    for key in keys:
        height_key = [0 for _ in range(5)]
        for line in key:
            for i, c in enumerate(line):
                if c == "#":
                    height_key[i] += 1
        height_based_keys.append(height_key)
    p1 = 0

    for key, lock in product(height_based_keys, height_based_locks):
        match = True
        for k, l in zip(key, lock):
            if k + l > 5:
                match = False
                break
        if match:
            p1 += 1

    print(f"Part 1: {p1}")


if __name__ == "__main__":
    main()
