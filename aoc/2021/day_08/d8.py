from aoc.cli import file_input
import pprint


SIMPLE_NUMBER_SEGMENT_COUNTS = {
    2,
    4,
    3,
    7,
}


SEGMENT_COUNTS = {
    2: (1,),
    3: (7,),
    4: (4,),
    5: (2, 3, 5),
    6: (0, 6, 9),
    7: (8,),
}


DEFAULT_SEGMENTS = {
    0: set(list("abcefg")),
    1: set(list("cf")),
    2: set(list("acdeg")),
    3: set(list("acdfg")),
    4: set(list("bcdf")),
    5: set(list("abdfg")),
    6: set(list("abdefg")),
    7: set(list("acf")),
    8: set(list("abcdefg")),
    9: set(list("abcdfg")),
}


NUMS_USING_SEGMENT = {
    "a": {0, 2, 3, 5, 6, 7, 8, 9},
    "b": {0, 4, 5, 6, 8, 9},
    "c": {0, 1, 2, 3, 4, 7, 8, 9},
    "d": {2, 3, 4, 5, 6, 8, 9},
    "e": {0, 2, 6, 8},
    "f": {0, 1, 3, 4, 5, 6, 7, 8, 9},
    "g": {0, 2, 3, 5, 6, 8, 9},
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
        # segment_map = {}
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

        # well i didn't need to do any of this masking i guess lol
        # segment_map["a"] = seven - one
        # segment_map["b"] = five - three
        # segment_map["c"] = one - five
        # segment_map["d"] = eight - zero
        # segment_map["e"] = two - three
        # segment_map["f"] = three - two
        # segment_map["g"] = eight - (seven | four | segment_map["a"] | segment_map["e"])

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
