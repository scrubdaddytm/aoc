from aoc.cli import file_input
from dataclasses import dataclass


def main() -> None:
    lines = []
    with file_input() as file:
        while line := file.readline():
            lines.append(line.strip())

    bits = bit_counter(lines)

    mid_bit_count = len(lines) / 2
    gamma_bits = []
    epsilon_bits = []
    for count in bits:
        if count > mid_bit_count:
            gamma_bits.append("1")
            epsilon_bits.append("0")
        else:
            gamma_bits.append("0")
            epsilon_bits.append("1")
    gamma = bits_to_int(gamma_bits)
    epsilon = bits_to_int(epsilon_bits)
    print(f"part 1: g={gamma} * e={epsilon} = {gamma * epsilon}")

    o2_candidates = lines
    co2_candidates = lines
    for i in range(len(lines[0])):
        if len(o2_candidates) > 1:
            o2_bits = bit_counter(o2_candidates)
            remaining_o2_candidates = []
            for line in o2_candidates:
                bit_criteria = "1" if o2_bits[i] >= (len(o2_candidates) / 2) else "0"
                if line[i] == bit_criteria:
                    remaining_o2_candidates.append(line)
            o2_candidates = remaining_o2_candidates
        if len(co2_candidates) > 1:
            co2_bits = bit_counter(co2_candidates)
            remaining_co2_candidates = []
            for line in co2_candidates:
                bit_criteria = "0" if co2_bits[i] >= (len(co2_candidates) / 2) else "1"
                if line[i] == bit_criteria:
                    remaining_co2_candidates.append(line)
            co2_candidates = remaining_co2_candidates

    o2 = bits_to_int(o2_candidates[0])
    co2 = bits_to_int(co2_candidates[0])
    print(f"part 2: o2={o2} * co2={co2} = {o2 * co2}")

def bits_to_int(bits: list) -> int:
    val = 0
    for bit in bits:
        val <<= 1
        if bit == "1":
            val |= 1
    return val


def bit_counter(bit_list: list[str]) -> list[int]:
    bits = [0 for _ in range(len(bit_list[0]))]
    for line in bit_list:
        for i, bit in enumerate(line):
            bits[i] += int(bit)
    return bits


if __name__ == "__main__":
    main()
