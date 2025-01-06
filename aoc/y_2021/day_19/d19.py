from aoc.cli import file_input
from aoc.geometry import Point3D


def main() -> None:
    scanners = []
    with file_input() as file:
        beacons = None
        while line := file.readline():
            if line[0:3] == "---":
                beacons = []
            while line := file.readline().strip():
                beacons.append(Point3D.from_list(line.split(",")))
            scanners.append(beacons)

    oriented_scanners = [[] for _ in range(100)]
    for beacon in scanners[0]:
        for idx, reoriented_beacon in enumerate(beacon.all_orientations()):
            oriented_scanners[idx].append(reoriented_beacon)

    for num, scanner in enumerate(oriented_scanners):
        if scanner:
            print(f"--- scanner {num} ---")
            for beacon in scanner:
                print(f"{beacon}")
            print()

    for num, scanner in enumerate(scanners):
        print(f"--- scanner {num} --- {scanner in oriented_scanners}")
        for beacon in scanner:
            print(f"{beacon}")
        print()


if __name__ == "__main__":
    main()
