from aoc.cli import file_input
from dataclasses import dataclass
from dataclasses import field
from copy import deepcopy


@dataclass(unsafe_hash=True)
class LinkedList:
    val: int = field(hash=True)
    original_idx: int = field(hash=True)
    p: "LinkedList" = field(hash=False, compare=False, default=None)
    n: "LinkedList" = field(hash=False, compare=False, default=None)

    def __repr__(self) -> str:
        return f"{self.p.val if self.p else None} <-> {self.val} <-> {self.n.val if self.n else None}"


def generate_linked_list(file: list[int]) -> tuple[LinkedList, dict[int, LinkedList]]:
    start = p = LinkedList(file[0], 0)
    position = {(file[0], 0): p}
    for idx, val in enumerate(file[1:-1], 1):
        entry = LinkedList(val, idx, p=p)
        p.n = entry
        p = entry
        position[(val, idx)] = entry
    final = LinkedList(file[-1], len(file) - 1)
    final.p = p
    final.n = start
    position[(final.val, final.original_idx)] = final
    p.n = final
    start.p = final
    return start, position


def print_ll(start: LinkedList, count: int | None = None):
    print_str = ""
    if count:
        for _ in range(count // 2):
            start = start.p
        print_str = "..."
    seen = set()
    c = 0
    while not start in seen:
        if count and c > count:
            break
        seen.add(start)
        print_str += f"{start.val}, "
        start = start.n
        c += 1
    print(f"{print_str[:-2]}{'...' if count else ''}\n")


def get_distance(v, size):
    size -= 1
    if v == 0 or v % size == 0:
        return 0
    return v % size if v > 0 else size + (v % -size)


def mix(file: list[int], position: dict[tuple[int, int], LinkedList]) -> int:
    size = len(file)
    zero = None
    for idx, val in enumerate(file):
        list_entry = position[(val, idx)]
        if val == 0:
            zero = list_entry

        distance = get_distance(list_entry.val, size)

        if distance == 0:
            print(f"{val} does not move")
            continue

        print(f"{val} moves {distance} spaces forward")

        # Connect the homies
        list_entry.p.n = list_entry.n
        list_entry.n.p = list_entry.p

        new_p = list_entry
        for _ in range(distance):
            new_p = new_p.n

        new_n = new_p.n
        new_n.p = list_entry
        new_p.n = list_entry
        list_entry.p = new_p
        list_entry.n = new_n

        print(f"moving {val} between {list_entry.p.val} and {list_entry.n.val}")
        if size < 20:
            print_ll(list_entry)

    start = zero
    print(f"{zero.p}{zero.n}")
    result = []
    for distance in range(0, 3001):
        if distance > 0 and distance % 1000 == 0:
            result.append(start.val)
        start = start.n
    return result


def main() -> None:
    file = []
    decryption_key = 811589153
    with file_input() as file_io:
        while line := file_io.readline():
            file.append(int(line))

    print(f"length of {len(file)} but count = {len(set(file))}")
    _, position = generate_linked_list(file)

    print(f"part1: {sum(mix(file, position))}")

    for idx in range(len(file)):
        file[idx] = file[idx] * decryption_key

    _, position = generate_linked_list(file)
    result = 0
    for _ in range(10):
        result = mix(file, position)
    print(f"part2: {sum(result)}")


if __name__ == "__main__":
    main()
