from aoc.cli import file_input


SIMPLE_NUMBER_SEGMENT_COUNTS = {
    2,
    4,
    3,
    7,
}


def main() -> None:
    lines = []
    with file_input() as file:
        while line := file.readline().strip():
            split_line = line.split(" | ")
            lines.append((split_line[0].split(), split_line[1].split()))

    easy_numbers = 0
    for patterns, outputs in lines:
        for output in outputs:
            if len(output) in SIMPLE_NUMBER_SEGMENT_COUNTS:
                easy_numbers += 1

    print(f"part 1: {easy_numbers=}")

    total = 0
    for patterns, outputs in lines:
        patterns = [
            set(list(pattern)) for pattern in sorted(patterns, key=lambda x: len(x))
        ]

        one = patterns[0]
        seven = patterns[1]
        four = patterns[2]
        eight = patterns[-1]

        fivers = patterns[3:6]
        three = None
        for fiver in fivers:
            if one < fiver:
                three = fiver
        fivers.remove(three)

        sixers = patterns[6:9]
        six = None
        for sixer in sixers:
            if not (one < sixer):
                six = sixer
        sixers.remove(six)

        zero = two = five = nine = None

        for fiver in fivers:
            if fiver < six:
                five = fiver
            else:
                two = fiver

        for sixer in sixers:
            if five < sixer:
                nine = sixer
            else:
                zero = sixer

        translator = {
            "".join(sorted(zero)): 0,
            "".join(sorted(one)): 1,
            "".join(sorted(two)): 2,
            "".join(sorted(three)): 3,
            "".join(sorted(four)): 4,
            "".join(sorted(five)): 5,
            "".join(sorted(six)): 6,
            "".join(sorted(seven)): 7,
            "".join(sorted(eight)): 8,
            "".join(sorted(nine)): 9,
        }

        number = 0
        for output in outputs:
            number *= 10
            number += translator["".join(sorted(output))]
        total += number
    print(f"part 2: {total=}")


if __name__ == "__main__":
    main()
