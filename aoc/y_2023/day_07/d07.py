from aoc.cli import file_input
from collections import defaultdict


CARD_VALUES = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
}
CARD_VALUES_P2 = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 1,
    "T": 10,
}


def card_value_p1(card: chr) -> int:
    if card and card.isdigit():
        return int(card)
    return CARD_VALUES[card]


def card_value_p2(card: chr) -> int:
    if card and card.isdigit():
        return int(card)
    return CARD_VALUES_P2[card]


def base_hand_value(hand: str, card_value: callable) -> int:
    return (
        (10**8) * card_value(hand[0])
        + (10**6) * card_value(hand[1])
        + (10**4) * card_value(hand[2])
        + (10**2) * card_value(hand[3])
        + card_value(hand[4])
    )


def hand_value(hand: str, card_value: callable = card_value_p1) -> int:
    cards = defaultdict(int)
    for card in hand:
        cards[card] += 1
    unique_cards = len(cards.keys())
    if unique_cards == 1:
        return (10**20) + base_hand_value(hand, card_value)
    elif unique_cards == 2:
        four_of_a_kind = False
        for card, count in cards.items():
            if count == 4:
                four_of_a_kind = True
                break
        if four_of_a_kind:
            return (10**18) + base_hand_value(hand, card_value)
        else:
            return (10**16) + base_hand_value(hand, card_value)
    elif unique_cards == 3:
        three_of_a_kind = False
        for card, count in cards.items():
            if count == 3:
                three_of_a_kind = True
                break
        if three_of_a_kind:
            return (10**14) + base_hand_value(hand, card_value)
        return (10**12) + base_hand_value(hand, card_value)
    elif unique_cards == 4:
        return (10**10) + base_hand_value(hand, card_value)

    return base_hand_value(hand, card_value)


def hand_value_p2(hand: str) -> int:
    cards = defaultdict(int)
    for card in hand:
        cards[card] += 1

    if cards["J"] == 0 or cards["J"] == 5:
        return hand_value(hand, card_value_p2)

    j_count = cards.pop("J")
    counts = list(reversed(sorted(cards.values())))

    if counts[0] + j_count == 5:
        return (10**20) + base_hand_value(hand, card_value_p2)
    elif counts[0] + j_count == 4:
        return (10**18) + base_hand_value(hand, card_value_p2)
    elif counts[0] + j_count == 3:
        if counts[1] == 2:
            return (10**16) + base_hand_value(hand, card_value_p2)
        else:
            return (10**14) + base_hand_value(hand, card_value_p2)
    elif counts[0] + j_count == 2:
        return (10**10) + base_hand_value(hand, card_value_p2)
    raise ValueError()


def main() -> None:
    hands_and_bids = {}
    with file_input() as file:
        while line := file.readline():
            hand, bid = line.split()
            hands_and_bids[hand] = int(bid)

    hands_ranked = sorted(hands_and_bids.keys(), key=hand_value)

    total_winnings = []
    for rank, hand in enumerate(hands_ranked):
        print(f"{rank+1} - {hand}, {hands_and_bids[hand]}")
        total_winnings.append((rank + 1) * hands_and_bids[hand])
    print(f"Part 1: {sum(total_winnings)}")

    hands_ranked_p2 = sorted(hands_and_bids.keys(), key=hand_value_p2)
    total_winnings = []
    for rank, hand in enumerate(hands_ranked_p2):
        print(f"{rank+1} - {hand}, {hands_and_bids[hand]}")
        total_winnings.append((rank + 1) * hands_and_bids[hand])
    print(f"Part 2: {sum(total_winnings)}")


if __name__ == "__main__":
    main()
