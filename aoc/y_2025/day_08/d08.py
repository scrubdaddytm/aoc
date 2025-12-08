import heapq
import math
from dataclasses import dataclass

from aoc.cli import file_input


@dataclass
class SetEntry[T]:
    parent: T
    size: int


class DisjointSet:
    """Followed the Union-Find wiki"""

    forest = None

    def __init__(self):
        self.forest = {}

    def find(self, item):
        if item not in self.forest:
            self.forest[item] = SetEntry(item, 1)

        while self.forest[item].parent != item:
            self.forest[item].parent = self.forest[self.forest[item].parent].parent
            item = self.forest[item].parent
        return item

    def size(self, item):
        return self.forest[self.find(item)].size

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)

        if a == b:
            return

        if self.forest[a].size < self.forest[b].size:
            a, b = b, a

        self.forest[b].parent = a
        self.forest[a].size = self.forest[a].size + self.forest[b].size


def distance(a, b) -> int:
    return math.sqrt(
        math.pow(
            a[0] - b[0],
            2,
        )
        + math.pow(
            a[1] - b[1],
            2,
        )
        + math.pow(
            a[2] - b[2],
            2,
        )
    )


def main() -> None:
    boxes = []
    with file_input() as file:
        while line := file.readline().strip():
            boxes.append(tuple(map(int, line.split(","))))

    boxes = sorted(boxes)

    p1 = 1
    p2 = 0

    heap = []
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            d = distance(boxes[i], boxes[j])
            heapq.heappush(heap, [d, boxes[i], boxes[j]])

    i = 0
    dj = DisjointSet()
    while len(heap) > 0:
        d, a, b = heapq.heappop(heap)

        dj.union(a, b)
        if dj.size(a) == len(boxes) or dj.size(b) == len(boxes):
            p2 = a[0] * b[0]
            break

        i += 1
        if i == 1000:
            top_3 = sorted(dj.forest.values(), key=lambda x: -x.size)[:3]
            for top in top_3:
                p1 *= top.size

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
