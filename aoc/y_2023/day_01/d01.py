from aoc.cli import file_input
import regex as re


VALID_DIGITS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def convert_to_int(val: str) -> int:
    if len(val) > 1:
        return VALID_DIGITS[val]
    return int(val)


def main() -> None:
    lines = []
    pattern = re.compile(r"\d|one|two|three|four|five|six|seven|eight|nine")
    with file_input() as file:
        while line := file.readline().strip():
            match = pattern.findall(line, overlapped=True)
            left = convert_to_int(match[0])
            right = convert_to_int(match[-1])
            print(f"{line} -> {left}, {right}")
            lines.append((10 * left) + right)
    print(f"{sum(lines)}")


if __name__ == "__main__":
    main()
