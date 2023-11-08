from aoc.cli import file_input


A = ord("A")
Z = ord("Z")
a = ord("a")
z = ord("z")


def value(item: chr) -> int:
    item_ord = ord(item)
    if item_ord >= a and item_ord <= z:
        return item_ord - a + 1
    elif item_ord >= A and item_ord <= Z:
        return item_ord - A + 27
    raise ValueError(f"how did we get a bad character - {item=}")


def priority_round_2(rucksacks: list[str]) -> int:
    prio_sum = 0
    for idx in range(0, len(rucksacks), 3):
        intersection = (
            set(rucksacks[idx]) &
            set(rucksacks[idx+1]) &
            set(rucksacks[idx+2])
        )
        prio_sum += value(intersection.pop())
    return prio_sum


def priority_round_1(rucksacks: list[str]) -> int:
    prio_sum = 0
    for rucksack in rucksacks:
        half = len(rucksack) // 2
        intersection = set(rucksack[:half]) & set(rucksack[half:])
        prio_sum += value(intersection.pop())
    return prio_sum


def main() -> None:
    rucksacks = []
    with file_input() as file:
        while line := file.readline().strip():
            rucksacks.append(line)

    prio_sum_round_1 = priority_round_1(rucksacks)
    print(f"{prio_sum_round_1=}")

    prio_sum_round_2 = priority_round_2(rucksacks)
    print(f"{prio_sum_round_2=}")


if __name__ == "__main__":
    main()
