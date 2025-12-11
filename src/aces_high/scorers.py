from itertools import combinations
from typing import List, Tuple

from .deck import Card


full_house_types = {
    'three_low': 0,
    'three_high': 1
}


class PokerHands:
    HIGH_CARD = 0
    PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9

    @staticmethod
    def get_all() -> List[str]:
        return ['HIGH_CARD', 'PAIR', 'TWO_PAIR', 'THREE_OF_A_KIND', 'STRAIGHT',
                'FLUSH', 'FULL_HOUSE', 'FOUR_OF_A_KIND', 'STRAIGHT_FLUSH', 'ROYAL_FLUSH']

    @classmethod
    def get(cls, name: str) -> int:
        return cls.__getattribute__(cls, name)

    @classmethod
    def get_by_value(cls, value: int) -> str:
        values_with_hand = {cls.get(hand): hand for hand in cls.get_all()}
        return values_with_hand[value]


def get_combinations(items: list, item_count: int):
    combos = []

    def generate_combinations(count: int, start: int, combo: list):
        count -= 1
        for i in range(start, len(items)):
            combo[count] = items[i]
            if count == 0:
                combos.append(combo[:])
            else:
                start += 1
                generate_combinations(count, start, combo)

    generate_combinations(item_count, 0, [0 for _ in range(item_count)])

    return combos


def get_v3(items: list):
    combos = []
    for i in range(0, len(items) - 2):
        for j in range(i + 1, len(items) - 1):
            for k in range(j + 1, len(items)):
                combos.append([items[i], items[j], items[k]])
    return combos


def get_combinations_v2(items: list, item_count: int, start: int = 0):
    combos = []

    if start + item_count > len(items):
        return

    current = items[start:start + item_count]
    rest = items[start + item_count:]

    get_combinations_v2(items, item_count, start + 1)

    return combos


def find_best_poker_hand(cards: list) -> Tuple[list, int]:
    possible_hands = combinations(cards, 5)
    hands_with_score = []
    for hand in possible_hands:
        score = score_poker_hand(hand)
        hands_with_score.append((hand, score))

    max_index = 0
    for i in range(len(hands_with_score)):
        if hands_with_score[i][1] > hands_with_score[max_index][1]:
            max_index = i

    return hands_with_score[max_index]


def score_poker_hand(cards: list) -> int:
    temp_cards = sorted(cards, key=lambda card: card.value)
    values = {c1.face: sum(1 for c2 in cards if c1.value == c2.value) for c1 in cards}
    suits = {card.suit for card in cards}
    value_count = len(values)

    if value_count == 5:
        is_straight = is_a_poker_straight(temp_cards)
        is_flush = len(suits) == 1

        if not is_straight and not is_flush:
            return PokerHands.HIGH_CARD
        if is_straight and is_flush:
            return PokerHands.ROYAL_FLUSH \
                if contains_ace(temp_cards) and contains_king(temp_cards) \
                else PokerHands.STRAIGHT_FLUSH
        elif is_straight:
            return PokerHands.STRAIGHT
        elif is_flush:
            return PokerHands.FLUSH
    else:
        if value_count == 4:
            return PokerHands.PAIR
        if value_count == 3:
            is_two_pair = len([key for (key, value) in values.items() if value == 2]) == 2
            return PokerHands.TWO_PAIR if is_two_pair else PokerHands.THREE_OF_A_KIND
        if value_count == 2:
            is_four_kind = len([key for (key, value) in values.items() if value == 4]) > 0
            return PokerHands.FOUR_OF_A_KIND if is_four_kind else PokerHands.FULL_HOUSE


def score_cribbage_hand(cards: list, cut_card: Card = None, is_crib: bool = False) -> int:
    score = 0
    temp_cards = cards  # [card for card in cards]

    score += count_flush(temp_cards, is_crib, cut_card)

    if cut_card is not None:
        score += count_nobs_v2(temp_cards, cut_card)
        temp_cards.append(cut_card)

    sum_values = [c.value if c.value < 10 else 10 for c in temp_cards]
    values = [c.value for c in temp_cards]

    # this is a complicated statement.  It calculates the points for pairs, runs, and combos of 15 all in one loop
    # for efficiency
    runs_found = False
    for i in range(len(temp_cards), 1, -1):
        # calculate all sums for i number of cards.  Score 2 points for any sum of 15
        score += sum(2 for c in combinations(sum_values, i) if sum(c) == 15)

        if i == 2:
            set_points = sum(2 for x, y in combinations(values, 2) if x == y)
            score += set_points
        elif i > 2 and not runs_found:
            sorted_combos = [c for c in combinations(values, i)]
            runs = [True for sc in sorted_combos if (max(sc) - min(sc) + 1) == len(sc) and len(set(sc)) == len(sc)]
            score += len(runs) * i
            if len(runs) > 0:
                runs_found = True
    return score


def contains_ace(cards: list):
    return any([c.face == "Ace" for c in cards])


def contains_king(cards: list):
    return any([c.face == 'King' for c in cards])


def is_a_poker_straight(sorted_cards: list) -> bool:
    max_value = sorted_cards[-1].value
    min_value = sorted_cards[0].value

    if (max_value - min_value == 4) or (contains_ace(sorted_cards) and contains_king(sorted_cards)):
        start = 2 if contains_ace and contains_king else 1
        for i in range(start, len(sorted_cards)):
            if sorted_cards[i].value - sorted_cards[i - 1].value != 1:
                return False

        return True

    return False


def count_nobs(cards: list, turn_card: Card) -> int:
    nob_cards = [True for card in cards if card.face == "Jack" and card.suit == turn_card.suit]
    return 1 if any(nob_cards) else 0


def count_nobs_v2(cards: list, turn_card: Card) -> int:
    for card in cards:
        if card.face == "Jack" and card.suit == turn_card.suit:
            return 1
    return 0


def count_flush(cards: list, is_crib: bool, turn_card: Card = None) -> int:
    suits = set([card.suit for card in cards])

    if len(suits) == 1:
        if turn_card is not None and suits.pop() == turn_card.suit:
            return 5
        else:
            return 4 if not is_crib else 0

    return 0
