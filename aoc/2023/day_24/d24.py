from itertools import combinations
from aoc.cli import file_input
from aoc.geometry import Point3D
from aoc.print_tools import Color
import numpy as np


def determinant_2d(a: Point3D, b: Point3D) -> int:
    return (b.x * a.y) - (a.x * b.y)


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
    A, Av = rays[0]
    A = np.array([A.x, A.y, A.z])
    Av = np.array([Av.x, Av.y, Av.z])

    B, Bv = rays[1]
    B = np.array([B.x, B.y, B.z])
    Bv = np.array([Bv.x, Bv.y, Bv.z])

    C, Cv = rays[2]
    C = np.array([C.x, C.y, C.z])
    Cv = np.array([Cv.x, Cv.y, Cv.z])

    l_rock = -np.cross(A, Av) + np.cross(B, Bv)
    r_rock = -np.cross(A, Av) + np.cross(C, Cv)
    rock = np.concatenate((l_rock, r_rock))

    def xm(v):
        return np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])

    ul = xm(Av) - xm(Bv)
    bl = xm(Av) - xm(Cv)
    ur = xm(A) - xm(B)
    br = xm(A) - xm(C)

    m = []
    for i in range(3):
        m.append(np.concatenate((ul[i], ur[i])))
    for i in range(3):
        m.append(np.concatenate((bl[i], br[i])))
    m = np.array(m)

    print(f"{m=}")
    print(f"{rock=}")
    result = np.linalg.inv(m).dot(rock)
    print(f"{result=}")
    print(f"Part 2: {sum(result[:3])}")


if __name__ == "__main__":
    main()
