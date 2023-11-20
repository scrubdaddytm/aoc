from aoc.cli import file_input
from itertools import pairwise
from collections import defaultdict


def main() -> None:
    template = None
    pair_insertion = dict()
    with file_input() as file:
        template = file.readline().strip()
        file.readline()
        while line := file.readline().strip():
            pair, insertion = line.split(" -> ")
            # pair_insertion[pair] = pair[0] + insertion + pair[1]
            pair_insertion[pair] = insertion
    print(f"{template=}")
    print(f"{pair_insertion=}")

    for step in range(1, 11):
        new_tmpl = str(template[0])
        for pair in pairwise(template):
            new_tmpl += pair_insertion["".join(pair)]
            new_tmpl += pair[1]
        template = new_tmpl
        print(f"After step {step}: {template}")

    element_count = defaultdict(int)
    for element in template:
        element_count[element] += 1
    count_list = [
        (k, v) for k, v in sorted(element_count.items(), key=lambda item: item[1])
    ]
    print(f"most={count_list[-1]}, least={count_list[0]}")
    print(f"part 1: {count_list[-1][1] - count_list[0][1]}")


if __name__ == "__main__":
    main()
