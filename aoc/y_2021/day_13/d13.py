from aoc.cli import file_input
from aoc.geometry import Point
from aoc.print_tools import print_point_grid


def main() -> None:
    points = set()
    folds = []
    with file_input() as file:
        while (line := file.readline().strip()) != "":
            line = line.split(",")
            points.add(Point(int(line[0]), int(line[1])))
        while fold_line_text := file.readline().strip():
            fold = fold_line_text.split()[2]
            fold_axis, fold_val = fold.split("=")
            folds.append((fold_axis, int(fold_val)))
    print(f"{points=}")
    print(f"{folds=}")
    print_point_grid(points)

    points_after_first_fold = 0
    for fold_axis, fold_val in folds:
        print(f"folding on {fold_axis}={fold_val}")
        points_to_discard = set()
        points_to_add = set()
        for point in points:
            if fold_axis == "y":
                if point.y > fold_val:
                    points_to_discard.add(point)
                    diff = abs(point.y - fold_val)
                    points_to_add.add(Point(point.x, fold_val - diff))
            else:
                if point.x > fold_val:
                    points_to_discard.add(point)
                    diff = abs(point.x - fold_val)
                    points_to_add.add(Point(fold_val - diff, point.y))

        points -= points_to_discard
        points |= points_to_add
        print_point_grid(points)

        if points_after_first_fold == 0:
            points_after_first_fold = len(points)

    print(f"part 1: points after first fold {points_after_first_fold}")
    # part 2 is in the final print output


if __name__ == "__main__":
    main()
