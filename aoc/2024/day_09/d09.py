from copy import copy
from dataclasses import dataclass

from aoc.cli import file_input


@dataclass
class Block:
    id: int
    size: int
    type: str
    next: "Block | None" = None
    prev: "Block | None" = None

    def insert_before(self, b: "Block") -> None:
        prev = self.prev
        prev.next = b
        b.prev = prev
        b.next = self
        self.prev = b

    def remove(self) -> None:
        prev = self.prev
        n = self.next
        prev.next = n
        n.prev = prev
        self.prev = None
        self.next = None
        self.id = -2
        self.type = "REMOVED"

    def __repr__(self) -> str:
        return f"{(self.name()) * self.size}"

    def name(self) -> str:
        if self.type == "EMPTY":
            return "."
        if self.id < 10:
            return str(self.id)
        return chr(self.id - 10 + ord("a"))

    def print_seq(self) -> None:
        b = self
        pstr = ""
        while b is not None:
            pstr += str(b)
            b = b.next
        print(pstr)


def parse(disk_map: str) -> tuple[list[Block], list[int]]:
    blocks = []
    gross = []
    i = 0
    alternator = True
    prev = None
    for c in disk_map:
        size = int(c)
        if alternator:
            blocks.append(Block(id=i, size=size, type="FILE"))
            gross.extend([i for _ in range(size)])
            i += 1
        elif size > 0:
            blocks.append(Block(id=-1, size=size, type="EMPTY"))
            gross.extend([-1 for _ in range(size)])
        blocks[-1].prev = prev
        if prev:
            prev.next = blocks[-1]
        prev = blocks[-1]
        alternator = not alternator
    return blocks, gross


def defragment_compact(blocks: list[Block], debug_enabled: bool = False) -> int:
    start = 0
    end = len(blocks) - 1
    while blocks[start] != -1:
        start += 1

    while start < end:
        blocks[start] = blocks[end]
        blocks[end] = -1

        while blocks[start] != -1:
            start += 1
        while blocks[end] == -1:
            end -= 1

    checksum = 0
    for i, ident in enumerate(blocks):
        if ident >= 0:
            checksum += i * ident

    return checksum


def defragment_whole_files(blocks: list[Block], debug_enabled: bool = False) -> int:
    start = blocks[0]
    if debug_enabled:
        start.print_seq()

    for block in reversed(blocks):
        if block.type != "FILE":
            continue

        empty = start
        while empty and (empty.type == "FILE" or empty.size < block.size):
            if empty.id == block.id:
                empty = None
            else:
                empty = empty.next

        if not empty:
            continue

        size_diff = empty.size - block.size

        block_copy = copy(block)
        empty.insert_before(block_copy)

        if size_diff > 0:
            empty.size = size_diff
        else:
            empty.remove()

        block.id = -1
        block.type = "EMPTY"
        if debug_enabled:
            start.print_seq()

    checksum = 0
    i = 0
    step = start
    while step:
        for _ in range(step.size):
            if step.id >= 0:
                checksum += i * step.id
            i += 1
        step = step.next
    return checksum


def main() -> None:
    blocks = []
    gross = []
    blocks_p2 = []
    with file_input() as file:
        while line := file.readline().strip():
            blocks, gross = parse(line)
            blocks_p2, _ = parse(line)

    debug_enabled = False

    p1_checksum = defragment_compact(gross, debug_enabled=debug_enabled)
    print(f"Part 1: {p1_checksum}")

    p2_checksum = defragment_whole_files(blocks, debug_enabled=debug_enabled)
    print(f"Part 2: {p2_checksum}")


if __name__ == "__main__":
    main()
