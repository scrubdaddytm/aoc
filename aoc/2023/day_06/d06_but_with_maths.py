from aoc.cli import file_input
import math


def main() -> None:
    rounds = []
    with file_input() as file:
        time = list(map(int, file.readline().strip().split(":")[1].split()))
        distance = list(map(int, file.readline().strip().split(":")[1].split()))
        time.append(int("".join(map(str, time))))
        distance.append(int("".join(map(str, distance))))
        rounds = list(zip(time, distance))

    counts = []
    for t, d in rounds:
        print(f"time={t}, distance={d}")
        discriminant = (t**2) - (4 * d)
        print(f"  {discriminant=}")
        d_sqrt = math.sqrt(discriminant)
        h1 = (t - d_sqrt) // 2
        h2 = (t + d_sqrt) // 2
        if math.floor(d_sqrt) ** 2 == discriminant:
            h2 -= 1
        print(f"  [{h1}, {h2}]")
        counts.append(int(h2 - h1))

    print(counts)
    print(f"Part 1: {math.prod(counts[:-1])}")
    print(f"Part 2: {counts[-1]}")


if __name__ == "__main__":
    main()
