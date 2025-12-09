import heapq
from itertools import pairwise

from aoc.cli import file_input
from aoc.geometry import LineSegment, Point, RectangleV2


def overlap(rect, segments) -> bool:
    for segment in segments:
        if segment.a in rect or segment.b in rect:
            return True

        if rect.is_on(segment.a) or rect.is_on(segment.b):
            if any([p in rect for p in segment.all_points()]):
                return True
            continue

        for wall in rect.lines():
            intersection = segment.point_intersection(wall)
            if intersection:
                return True
    return False


def main() -> None:
    tiles = []
    with file_input() as file:
        while line := file.readline().strip():
            tile = tuple(map(int, line.split(",")))
            tiles.append(Point(tile[0], tile[1]))

    p1 = 0
    p2 = 0

    heap = []
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            a = tiles[i]
            b = tiles[j]
            rect = RectangleV2(a, b)
            a = rect.area()
            heapq.heappush(heap, (-a, rect))
            p1 = max(p1, a)

    tiles.append(tiles[0])
    segments = []
    for a, b in pairwise(tiles):
        seg = LineSegment(a, b)
        segments.append(seg)

    while len(heap) > 0:
        p2, rect = heapq.heappop(heap)

        if not overlap(rect, segments):
            break

    print(f"Part 1: {p1}")
    print(f"Part 2: {-p2}")


if __name__ == "__main__":
    main()
