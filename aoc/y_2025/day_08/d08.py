import heapq
import math

from aoc.cli import file_input


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
        for j in range(i, len(boxes)):
            if i != j:
                d = distance(boxes[i], boxes[j])
                heapq.heappush(heap, [d, boxes[i], boxes[j]])

    circuits = {}
    for i in range(1000):
        d, a, b = heapq.heappop(heap)

        ab_c = None
        if a in circuits and b in circuits:
            a_c = circuits[a]
            b_c = circuits[b]
            ab_c = set(a_c) | set(b_c)
        elif a in circuits:
            ab_c = set(circuits[a])
        elif b in circuits:
            ab_c = set(circuits[b])
        else:
            ab_c = set()

        ab_c.add(a)
        ab_c.add(b)
        ab_c = frozenset(ab_c)
        for box in ab_c:
            circuits[box] = ab_c

    top_3 = sorted(set(circuits.values()), key=lambda x: -len(x))[:3]
    for top in top_3:
        p1 *= len(top)

    a = None
    b = None
    while len(heap) > 0:
        d, a, b = heapq.heappop(heap)

        ab_c = None
        if a in circuits and b in circuits:
            a_c = circuits[a]
            b_c = circuits[b]
            ab_c = set(a_c) | set(b_c)
        elif a in circuits:
            ab_c = set(circuits[a])
        elif b in circuits:
            ab_c = set(circuits[b])
        else:
            ab_c = set()

        ab_c.add(a)
        ab_c.add(b)
        if len(ab_c) == len(boxes):
            break
        ab_c = frozenset(ab_c)
        for box in ab_c:
            circuits[box] = ab_c

    p2 = a[0] * b[0]

    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    main()
