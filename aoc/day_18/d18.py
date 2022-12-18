from aoc.cli import file_input
from dataclasses import dataclass
from collections import deque


@dataclass(order=True, frozen=True)
class Point:
    x: int
    y: int
    z: int

    def connected(self, other: "Point") -> bool:
        x_diff = abs(self.x - other.x)
        y_diff = abs(self.y - other.y)
        z_diff = abs(self.z - other.z)
        return any([
            x_diff == 0 and y_diff == 0,
            x_diff == 0 and z_diff == 0,
            y_diff == 0 and z_diff == 0,
        ])

    def all_directions(self) -> list["Point"]:
        return [
            Point(self.x+1, self.y, self.z),
            Point(self.x-1, self.y, self.z),
            Point(self.x, self.y+1, self.z),
            Point(self.x, self.y-1, self.z),
            Point(self.x, self.y, self.z+1),
            Point(self.x, self.y, self.z-1),
        ]

    def __repr__(self) -> str:
        return f"{self.x, self.y, self.z}"


def add_to_space(space, point) -> None:
    space.setdefault(point.x, {}).setdefault(point.y, {}).setdefault(point.z, True)

def in_space(space, point) -> bool:
    return space.get(point.x, {}).get(point.y, {}).get(point.z, False)


def find_sets(points, neighbors) -> list[set[Point]]:
    bucketed = set()
    buckets = []
    for point in points:
        if point in bucketed:
            continue
        bucket = set()
        q = deque()
        q.append(point)
        bucket.add(point)
        while q:
            p = q.popleft()
            for n in neighbors.get(p, []):
                if not n in bucket:
                    bucket.add(n)
                    q.append(n)
        buckets.append(bucket)
        bucketed |= bucket
    return buckets


def get_surface_areas(connected_cubes, neighbors) -> list[int]:
    surface_areas = []
    for lava in connected_cubes:
        area = 0
        for point in lava:
            area += 6 - len(neighbors.get(point, []))
        surface_areas.append(area)
    return surface_areas


def get_neighbors(p) -> list[Point]:
    return [
        Point(p.x-1, p.y, p.z),
        Point(p.x+1, p.y, p.z),
        Point(p.x, p.y-1, p.z),
        Point(p.x, p.y+1, p.z),
        Point(p.x, p.y, p.z-1),
        Point(p.x, p.y, p.z+1),
    ]


def fill_gaps(points: set[Point]) -> None:
    xs = {p.x for p in points}
    ys = {p.y for p in points}
    zs = {p.z for p in points}
    min_x, max_x = min(xs)-1, max(xs)+1
    min_y, max_y = min(ys)-1, max(ys)+1
    min_z, max_z = min(zs)-1, max(zs)+1

    problem_space = set([Point(x, y, z) for x in range(min_x, max_x) for y in range(min_y, max_y) for z in range(min_z, max_z)])

    water = set()
    q = deque()
    start = Point(min_x, min_y, min_z)
    q.append(start)
    water.add(start)
    while q:
        p = q.popleft()
        for n in get_neighbors(p):
            if n in problem_space and not n in points and not n in water:
                water.add(n)
                q.append(n)
    print(f"ps: {len(problem_space)}, w: {len(water)}")
    points |= (problem_space - water) 

    
def total_surface_area(points: set[Point], should_fill_gaps: bool = False) -> list[int]:
    if should_fill_gaps:
        fill_gaps(points)
    neighbors = {}
    for p in points:
        for n in p.all_directions():
            if n in points:
                p_n = neighbors.setdefault(p, set())
                p_n.add(n)
                n_n = neighbors.setdefault(n, set())
                n_n.add(p)

    connected_cubes = find_sets(points, neighbors)
    # for cube in connected_cubes:
    #     print(f"{cube}")

    surface_areas = get_surface_areas(connected_cubes, neighbors)
    return sum(surface_areas)


def main() -> None:
    points = set()
    with file_input() as file:
        while line := file.readline().strip():
            spl = list(map(int, line.split(',')))
            points.add(Point(spl[0], spl[1], spl[2]))

    surface_areas = total_surface_area(points)
    print(f"Round 1: {surface_areas}")

    surface_areas = total_surface_area(points, True)
    print(f"Round 2: {surface_areas}")


if __name__ == "__main__":
    main()