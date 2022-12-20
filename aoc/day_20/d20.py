from aoc.cli import file_input
from dataclasses import dataclass
from dataclasses import field
from copy import deepcopy


@dataclass(unsafe_hash=True)
class LinkedList:
    val: int = field(hash=True)
    original_idx: int = field(hash=True)
    prev: "LinkedList" = field(hash=False, compare=False, default=None)
    next: "LinkedList" = field(hash=False, compare=False, default=None)
    def __repr__(self) -> str:
        return f"{self.prev.val if self.prev else None} <-> {self.val} <-> {self.next.val if self.next else None}"

    

def generate_linked_list(file: list[int]) -> tuple[LinkedList, dict[int, LinkedList]]:
    start = prev = LinkedList(file[0], 0)
    position = {file[0]: prev}
    for idx, val in enumerate(file[1:-1], 1):
        entry = LinkedList(val, idx, prev=prev)
        prev.next = entry
        prev = entry
        position[val] = entry
    final = LinkedList(file[-1], len(file)-1)
    final.prev = prev
    final.next = start
    position[final.val] = final
    prev.next = final
    start.prev = final
    return start, position


def print_ll(start: LinkedList, count: int | None = None):
    print_str = ""
    seen = set()
    c = 0
    while not start in seen:
        if count and c > count:
            break
        seen.add(start)
        print_str += f"{start.val}, "
        start = start.next
        c += 1
    print(f"{print_str[:-2]}")


def main() -> None:
    # I give the wrong output :(
    file = []
    with file_input() as file_io:
        while line := file_io.readline():
            file.append(int(line))
    print(f"{file}")
    print(f"length of {len(file)} but count = {len(set(file))}")
    linked_list, position = generate_linked_list(file)
    size = len(file)
    print_ll(position[0])
    for val in file:
        list_entry = position[val]
        left = list_entry.val < 0

        modulo = -size if left else size
        if list_entry.val % modulo == 0:
            print(f"{val} does not move")
            continue

        # Connect the homies
        list_entry.prev.next = list_entry.next
        list_entry.next.prev = list_entry.prev

        im_next = list_entry
        for _ in range(abs(list_entry.val % modulo)):
            if left:
                im_next = im_next.prev
            else:
                im_next = im_next.next

        if left:
            # print(f"moving {val} between {im_next.prev.val} and {im_next.val}")
            list_entry.next = im_next
            list_entry.prev = im_next.prev
            im_next.prev.next = list_entry
            im_next.prev = list_entry
        else:
            # print(f"moving {val} between {im_next.val} and {im_next.next.val}")
            list_entry.prev = im_next
            list_entry.next = im_next.next
            im_next.next.prev = list_entry
            im_next.next = list_entry
        print_ll(position[0], count=10)

    start = zero = position[0]
    print_ll(start)
    result = []
    for distance in [1000, 2000, 3000]:
        start = zero
        tru_distance = distance % size
        for _ in range(tru_distance):
            start = start.next
        result.append(start.val)
    print(f"{result=} sums to {sum(result)}")
    



if __name__ == "__main__":
    main()