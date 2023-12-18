from aoc.cli import file_input
from aoc.data_structures import PriorityQueue
from aoc.geometry import Point, left, right, up, down, in_bounds


DIRECTIONS = {
    right: [up, down],
    left: [up, down],
    up: [left, right],
    down: [left, right],
}
STR_TO_D = {
    "right": right,
    "left": left,
    "up": up,
    "down": down,
}


def lose_heat(graph: list[list[int]], direction_limit: int, min_movement: int = 1) -> int:
    start = Point(0, 0)
    bounds = Point(len(graph[0]), len(graph))
    target = Point(bounds.x - 1, bounds.y - 1)

    pq = PriorityQueue(pq_removed_item=(Point(-1, -1), "up"))
    score = {}
    seen = set()
    for d in ["right", "up"]:
        e = (start, d)
        score[e] = 0
        pq.add(e, 0)

    while pq:
        p, d = pq.pop()

        heat = score[(p, d)]
        if p == target:
            return heat
        if (p, d) in seen:
            continue
        seen.add((p, d))

        d = STR_TO_D[d]

        for next_d in DIRECTIONS[d]:
            heat_increase = 0
            curr = p
            for _ in range(1, min_movement):
                curr = d(curr)
                if not in_bounds(curr, max_x=bounds.x, max_y=bounds.y):
                    break
                heat_increase += graph[curr.y][curr.x]

            for _ in range(min_movement, direction_limit + 1):
                curr = d(curr)
                if not in_bounds(curr, max_x=bounds.x, max_y=bounds.y):
                    break

                heat_increase += graph[curr.y][curr.x]
                key = (curr, next_d.__name__)
                tent_score = heat + heat_increase
                if tent_score < score.get(key, 9999999999999):
                    score[key] = tent_score
                    pq.add((curr, next_d.__name__), tent_score)


def main() -> None:
    graph = []
    with file_input() as file:
        while line := file.readline().strip():
            graph.append(list(map(int, line)))

    print(f"Part 1: {lose_heat(graph, 3)}")
    print(f"Part 1: {lose_heat(graph, 10, 4)}")


if __name__ == "__main__":
    main()
