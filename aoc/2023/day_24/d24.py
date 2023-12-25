from itertools import combinations
from aoc.cli import file_input
from aoc.geometry import Point3D
from aoc.print_tools import Color
import numpy as np


def determinant_2d(a: Point3D, b: Point3D) -> int:
    return (b.x * a.y) - (a.x * b.y)


def cross_matrix(vector):
    return np.array([[0, -vector[2], vector[1]], [vector[2], 0, -vector[0]], [-vector[1], vector[0], 0]])


def main() -> None:
    rays = []
    with file_input() as file:
        while line := file.readline().strip():
            point, vector = line.split(" @ ")
            point = list(map(int, point.split(", ")))
            vector = list(map(int, vector.split(", ")))
            rays.append((Point3D(point[0], point[1], point[2]), Point3D(vector[0], vector[1], vector[2])))

    # bound = (7, 27)
    bound = (200000000000000, 400000000000000)

    intersections = 0
    for (A, vA), (B, vB) in combinations(rays, 2):
        # print(f"Hailstone A: {A} @ {vA}")
        # print(f"Hailstone B: {B} @ {vB}")
        vector_determinant = determinant_2d(vA, vB)
        if vector_determinant == 0:
            # print(" --- " + Color.YELLOW + "Parallel!" + Color.END)
            continue

        u = B.y - A.y
        u += (vB.y * A.x) / vB.x
        u -= (vB.y * B.x) / vB.x
        u /= vA.y - (vB.y * vA.x) / vB.x

        v = (A.x + vA.x * u - B.x) / vB.x

        if u >= 0 and v >= 0:
            cX = A.x + vA.x * u
            cY = A.y + vA.y * u
            if bound[0] <= cX <= bound[1] and bound[0] <= cY <= bound[1]:
                # print(" --- " + Color.GREEN + "Inside!" + Color.END + f" @ ({cX}, {cY})")
                intersections += 1
            # else:
            #     print(" --- " + Color.RED + "Outside!" + Color.END + f" @ ({cX}, {cY})")
        # else:
        # print(" --- " + Color.BLUE + "No Intersection!" + Color.END)
        # print()

    print(f"Part 1: {intersections}")

    # Rock and rock velocity are our unknowns. Perform Gaussian elimination.
    results = []
    sums = []
    for x in range(100):
        three_rays = []
        for P, V in rays[x:x+3]:
            three_rays.append(np.array([P.x, P.y, P.z]))
            three_rays.append(np.array([V.x, V.y, V.z]))

        A, Av, B, Bv, C, Cv = three_rays

        l_rock = -np.cross(A, Av) + np.cross(B, Bv)
        r_rock = -np.cross(A, Av) + np.cross(C, Cv)
        rock = np.concatenate((l_rock, r_rock))

        ul = cross_matrix(Av) - cross_matrix(Bv)
        bl = cross_matrix(Av) - cross_matrix(Cv)
        ur = cross_matrix(A) - cross_matrix(B)
        br = cross_matrix(A) - cross_matrix(C)

        m = []
        for i in range(3):
            m.append(np.concatenate((ul[i], ur[i])))
        for i in range(3):
            m.append(np.concatenate((bl[i], br[i])))
        m = np.array(m)

        # print(f"{m=}")
        # print(f"{rock=}")
        result = np.linalg.inv(m).dot(rock)
        # print(f"{result=}")
        sums.append(sum(result[:3]))
        results.append(result[:3])
    sums = list(sorted(set(sums)))
    for idx, result in enumerate(results):
        if int(result[0]) == result[0] and int(result[1]) == result[1] and int(result[2]) == result[2]:
            print(f"Part 2: {idx} -> {sum(result)} <- {result}")


if __name__ == "__main__":
    main()
