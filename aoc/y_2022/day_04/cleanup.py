from dataclasses import dataclass

from aoc.cli import file_input


@dataclass
class Pair:
    left: int
    right: int


def contains(section_a: Pair, section_b: Pair) -> bool:
    return (
        section_a.left <= section_b.left and 
        section_a.right >= section_b.right
    )


def overlaps(section_a: Pair, section_b: Pair) -> bool:
    return (
        (section_a.left >= section_b.left and section_a.left <= section_b.right) or
        (section_a.right >= section_b.left and section_a.right <= section_b.right)
    )


def count(assignments: list[list[Pair]], comparator: callable) -> int:
    overlap_count = 0
    for pairs in assignments:
        if (
            comparator(pairs[0], pairs[1]) or
            comparator(pairs[1], pairs[0])
        ):
            overlap_count += 1
    return overlap_count


def main() -> None:
    assignments = []
    with file_input() as file:
        while line := file.readline().strip():
            pairs_raw = line.split(",")
            pairs = []
            for pair in pairs_raw:
                pair_split = pair.split("-")
                pairs.append(Pair(int(pair_split[0]), int(pair_split[1])))
            assignments.append(pairs)

    contains_count = count(assignments, contains)
    print(f"{contains_count=}")

    overlap_count = count(assignments, overlaps)
    print(f"{overlap_count=}")


if __name__ == "__main__":
    main()
