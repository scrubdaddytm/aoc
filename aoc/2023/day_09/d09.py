from aoc.cli import file_input
from dataclasses import dataclass
from itertools import pairwise


def main() -> None:
    lines = []
    with file_input() as file:
        while line := file.readline():
            lines.append(list(map(int, line.strip().split())))

    all_values = 0
    prepended_values = 0
    for sequence in lines:
        print(f"SEQUENCE: {sequence}")
        next_seqs = [sequence]
        while not all(v == 0 for v in next_seqs[-1]):
            next_seqs.append([b - a for a, b in pairwise(next_seqs[-1])])

        print(f"ALL SEQ: {next_seqs}")
        next_seqs = list(reversed(next_seqs))
        for idx in range(1, len(next_seqs)):
            seq = next_seqs[idx - 1]
            next_seq = next_seqs[idx]
            print(f"ADDING {seq[-1]} + {next_seq[-1]}")
            next_seq.append(seq[-1] + next_seq[-1])
            next_seq.insert(0, next_seq[0] - seq[0])

        print(f"ADDED TO ALL SEQ: {list(reversed(next_seqs))}")
        all_values += next_seqs[-1][-1]
        prepended_values += next_seqs[-1][0]
    print(f"Part 1: {all_values=}")
    print(f"Part 2: {prepended_values=}")


if __name__ == "__main__":
    main()
