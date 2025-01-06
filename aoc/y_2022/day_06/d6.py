from aoc.cli import file_input


def find_start(signal: str, dcs: int) -> int:
    for i in range(len(signal)-dcs):
        seq = signal[i:i+dcs]
        if len(set(seq)) == dcs:
            return i+dcs


def main() -> None:
    thing = []
    with file_input() as file:
        while line := file.readline().strip():
            thing.append(line)

    for line in thing:
        start = find_start(line, 4)
        print(f"{start=}")

    for line in thing:
        start = find_start(line, 14)
        print(f"r2: {start=}")
    print(f"{int(1)}")


if __name__ == "__main__":
    main()