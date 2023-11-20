from aoc.cli import file_input
from itertools import pairwise
from collections import defaultdict


def main() -> None:
    template = None
    rules = dict()
    with file_input() as file:
        template = file.readline().strip()
        file.readline()
        while line := file.readline().strip():
            pair, insertion = line.split(" -> ")
            rules[pair] = insertion
    print(f"{template=}")
    print(f"{rules=}")

    score = defaultdict(int)
    pair_count = defaultdict(int)

    for pair in pairwise(template):
        pair_count[pair] += 1

    for char in template:
        score[char] += 1

    for step in range(1, 41):
        new_pair_count = defaultdict(int)
        for (left, right), count in pair_count.items():
            pair = left + right
            inserted_char = rules[pair]

            new_pair_count[pair] -= count
            new_pair_count[left + inserted_char] += count
            new_pair_count[inserted_char + right] += count

            score[inserted_char] += count

        for pair, count in new_pair_count.items():
            pair_count[pair] += count

        if step == 10:
            print(f"part 1: {max(score.values()) - min(score.values())}")

    print(f"part 2: {max(score.values()) - min(score.values())}")


if __name__ == "__main__":
    main()
