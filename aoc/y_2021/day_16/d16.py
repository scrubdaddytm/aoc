from aoc.cli import file_input


HEX_TO_BINARY = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def get_version_sum(packet: tuple) -> int:
    version_sum = 0
    if not packet:
        return version_sum
    version_sum += packet[0]
    if packet[1] != 4:
        for sub_packet in packet[3]:
            version_sum += get_version_sum(sub_packet)
    return version_sum


def get_literal_value(binary: list[str]) -> int:
    bits = ""
    end_idx = None
    for idx in range(0, len(binary), 5):
        bits += binary[idx + 1 : idx + 5]
        if binary[idx] == "0":
            end_idx = idx + 5
            break
    return int(bits, 2), end_idx


def decode(binary: str) -> str:
    if not binary or int(binary, 2) == 0:
        return (None, None, None, None)

    version = int(binary[0:3], 2)
    packet_type = int(binary[3:6], 2)
    value = end_idx = None
    sub_packets = []

    if packet_type != 4:
        length_type_id = binary[6]
        if length_type_id == "0":
            sub_packet_bits = int(binary[7:22], 2)
            sub_packet_start = 22
            while sub_packet_start < 22 + sub_packet_bits:
                sub_packet = decode(binary[sub_packet_start:])
                if sub_packet[-1]:
                    sub_packet_start += sub_packet[-1]
                else:
                    break
                sub_packets.append(sub_packet)
            end_idx = sub_packet_start
        else:
            sub_packet_count = int(binary[7:18], 2)
            sub_packet_start = 18
            for packet_count in range(sub_packet_count):
                sub_packet = decode(binary[sub_packet_start:])
                if sub_packet[-1]:
                    sub_packet_start += sub_packet[-1]
                else:
                    break
                sub_packets.append(sub_packet)
            end_idx = sub_packet_start

    if packet_type == 0:
        value = sum([sp[2] for sp in sub_packets])
    if packet_type == 1:
        value = 1
        for sp in sub_packets:
            value *= sp[2]
    if packet_type == 2:
        value = min([sp[2] for sp in sub_packets])
    if packet_type == 3:
        value = max([sp[2] for sp in sub_packets])
    elif packet_type == 4:
        value, end_idx = get_literal_value(binary[6:])
        end_idx += 6
    if packet_type == 5:
        value = 1 if sub_packets[0][2] > sub_packets[1][2] else 0
    if packet_type == 6:
        value = 1 if sub_packets[0][2] < sub_packets[1][2] else 0
    if packet_type == 7:
        value = 1 if sub_packets[0][2] == sub_packets[1][2] else 0

    return (version, packet_type, value, sub_packets, end_idx)


def main() -> None:
    encoded_packets = []
    with file_input() as file:
        while line := file.readline().strip():
            encoded_packets.append(line)
    print(f"{encoded_packets}")

    for encoded_packet in encoded_packets:
        binary = "".join(map(lambda c: HEX_TO_BINARY[c], list(encoded_packet)))
        packet = decode(binary)
        print(
            f"{encoded_packet}\n --> SUM: {get_version_sum(packet)}, VALUE: {packet[2]}"
        )
    # print(packets)


if __name__ == "__main__":
    main()
