from aoc.cli import file_input
import regex as re
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class Lens:
    name: str
    length: int | None = field(compare=False)

    def __repr__(self) -> str:
        return f"[{self.name} {self.length}]"


def hash(to_encode: str) -> int:
    result = 0
    for c in to_encode:
        result += ord(c)
        result *= 17
        result %= 256
    return result


def main() -> None:
    p1 = []
    with file_input() as file:
        while line := file.readline().strip():
            p1.extend(line.split(","))

    result = 0
    for value in p1:
        result += hash(value)

    print(f"Part 1: {result}")

    p2 = []
    pattern = re.compile(r"([a-z]+)(-|=)?(\d+)?")
    for entry in p1:
        operation = pattern.findall(entry)[0]
        length = None
        if operation[2]:
            length = int(operation[2])
        p2.append((Lens(operation[0], length), operation[1]))

    hashmap = defaultdict(list)
    for lens, op in p2:
        lenses = hashmap[hash(lens.name)]
        if op == "=":
            for box_lens in lenses:
                if lens == box_lens:
                    box_lens.length = lens.length
                    break
            else:
                hashmap[hash(lens.name)].append(lens)
        else:
            if lens in lenses:
                lenses.remove(lens)

    focusing_power = 0
    for num, items in sorted(hashmap.items()):
        if len(items) == 0:
            continue
        print(f"Box {num}: {' '.join(map(str, items))}")
        for idx, lens in enumerate(items):
            focusing_power += (num + 1) * (idx + 1) * lens.length

    print(f"Part 2: {focusing_power}")


if __name__ == "__main__":
    main()
