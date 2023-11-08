from aoc.cli import file_input
from dataclasses import dataclass


VALS = {
    3: "=",
    4: "-",
    0: "0",
    1: "1",
    2: "2",
}


def from_snafu(number: str) -> int:
    val = 0
    for idx, char in enumerate(reversed(number)):
        mult = pow(5, idx)
        if char == "2":
            val += 2 * mult
        elif char == "1":
            val += mult
        elif char == "-":
            val -= mult
        elif char == "=":
            val -= 2 * mult
    return val


def to_snafu(number: int) -> str:
    n = number
    snafu = ""
    while n > 0:
        val = n % 5
        snafu = VALS[val] + snafu
        n //= 5
        if val > 2:
            n += 1
    return snafu if snafu else "0"


def main() -> None:
    numbers = []
    with file_input() as file:
        while line := file.readline().strip():
            numbers.append(line)

    converted = []
    for number in numbers:
        converted.append(from_snafu(number))
        print(f"{number} -> {converted[-1]}")

    fuel_sum = sum(converted)
    print(f"sum: {fuel_sum}")
    print(f"sum as SNAFU: {to_snafu(fuel_sum)}")


if __name__ == "__main__":
    main()
