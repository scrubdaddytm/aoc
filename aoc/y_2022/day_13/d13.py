from aoc.cli import file_input
from typing import Any
from functools import cmp_to_key


def compare(packet_a: list[Any], packet_b: list[Any]) -> int:
    result = _compare(packet_a, packet_b)
    if result is True:
        return -1
    if result is False:
        return 1
    return 0

def _compare(packet_a: list[Any], packet_b: list[Any], depth: int = 0) -> bool | None:
    l_idx, r_idx = 0, 0
    while l_idx < len(packet_a) and r_idx < len(packet_b):
        l_val, r_val = packet_a[l_idx], packet_b[r_idx]
        print(f"{' '*depth}- Compare {l_val} vs {r_val}")
        if isinstance(l_val, int) and isinstance(r_val, int):
            if l_val > r_val:
                print(f"{' '*(depth+1)}- Right side is smaller. NOT in the right order")
                return False
            elif l_val < r_val:
                print(f"{' '*(depth+1)}- Right side is smaller. IN THE RIGHT ORDER")
                return True
        else:
            if isinstance(l_val, int) and isinstance(r_val, list):
                l_val = [l_val]
            elif isinstance(l_val, list) and isinstance(r_val, int):
                r_val = [r_val]
            result = _compare(l_val, r_val, depth+1)
            if result is not None:
                return result
            
        l_idx += 1
        r_idx += 1
    if l_idx < len(packet_a) and r_idx == len(packet_b):
        print(f"{' '*(depth+1)}- Right side ran out of items, NOT in the right order")
        return False
    if l_idx == len(packet_a) and r_idx < len(packet_b):
        print(f"{' '*(depth+1)}- Left side ran out of items, IN THE RIGHT ORDER")
        return True
    return None


def main() -> None:
    pairs = []
    all_packets = [[[2]],[[6]]]
    with file_input() as file:
        pair = []
        while line := file.readline():
            if line == "\n":
                pairs.append(pair)
                pair = []
            else:
                packet = eval(line.strip())
                pair.append(packet)
                all_packets.append(packet)
        pairs.append(pair)

    print(f"===== PART 1 =====")
    proper_ordered = 0
    for idx, pair in enumerate(pairs):
        print(f"== Pair {idx+1} ==")
        print(f"LEFT - {pair[0]}\nRIGHT - {pair[1]}")
        if compare(pair[0], pair[1]) == -1:
            proper_ordered += (idx+1)
    print(f"{proper_ordered=}")

    print(f"===== PART 2 =====")
    all_packets = sorted(all_packets, key=cmp_to_key(compare))
    key = 1
    for idx, packet in enumerate(all_packets):
        print(packet)
        if packet == [[2]]:
            key *= (idx+1)
        if packet == [[6]]:
            key *= (idx+1)
    print(f"{key=}")


if __name__ == "__main__":
    main()