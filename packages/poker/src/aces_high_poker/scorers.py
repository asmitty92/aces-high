from collections import Counter
from enum import Enum
from typing import TypeAlias, Optional

from aces_high_core import Card, Rank

from .pocker_card import PokerCard


class PokerResult(Enum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9


ScoreResult: TypeAlias = Optional[tuple[PokerResult, list[int]]]


def get_set_values(cards: list[Card], counts: Counter, set_length: int) -> list[int]:
    set_values = {card.value for card in cards if counts[card.rank] == set_length}
    kickers = {card.value for card in cards if counts[card.rank] == 1}
    return [*sorted(set_values, reverse=True), *sorted(kickers, reverse=True)]


def score_high_card(cards: list[Card], _) -> ScoreResult:
    sorted_cards = sorted(cards, key=lambda card: card.value, reverse=True)
    return PokerResult.HIGH_CARD, [card.value for card in sorted_cards]


def score_pair(cards: list[Card], counts: Counter) -> ScoreResult:
    if list(counts.values()).count(2) == 1 and len(counts) == 4:
        return PokerResult.PAIR, get_set_values(cards, counts, 2)
    return None


def score_two_pair(cards: list[Card], counts: Counter) -> ScoreResult:
    if list(counts.values()).count(2) == 2 and len(counts) == 3:
        return PokerResult.TWO_PAIR, get_set_values(cards, counts, 2)
    return None


def score_three_of_a_kind(cards: list[Card], counts: Counter) -> ScoreResult:
    if list(counts.values()).count(3) == 1 and len(counts) == 3:
        return PokerResult.THREE_OF_A_KIND, get_set_values(cards, counts, 3)
    return None


def score_full_house(cards: list[Card], counts: Counter) -> ScoreResult:
    if list(counts.values()).count(2) == 1 and list(counts.values()).count(3) == 1 and len(counts) == 2:
        three_card_value = get_set_values(cards, counts, 3)
        pair_value = get_set_values(cards, counts, 2)
        return PokerResult.FULL_HOUSE, [*three_card_value, *pair_value]


def score_four_of_a_kind(cards: list[Card], counts: Counter) -> ScoreResult:
    if list(counts.values()).count(4) == 1 and len(counts) == 2:
        return PokerResult.FOUR_OF_A_KIND, get_set_values(cards, counts, 4)


def contains_flush(cards: list[PokerCard]) -> bool:
    unique_suits = {card.suit for card in cards}
    return len(unique_suits) == 1


def contains_straight(cards: list[PokerCard], counts: Counter) -> tuple[bool, bool]:
    sorted_cards = sorted(cards, key=lambda card: card.value, reverse=True)
    has_king = any(card for card in cards if card.rank == Rank.KING)
    has_ace = any(card for card in cards if card.rank == Rank.ACE)

    is_standard_straight = (len(counts) == 5 and sorted_cards[0].value - sorted_cards[-1].value == 4)
    if is_standard_straight:
        return True, False
    is_ace_low_straight = (
            len(counts) == 5
            and has_ace
            and sorted_cards[1].value == 5
            and sorted_cards[1].value - sorted_cards[-1].value == 3)
    if is_ace_low_straight:
        return True, True
    is_ace_high_straight = (
            len(counts) == 5
            and has_king
            and has_ace
            and sorted_cards[0].value - sorted_cards[-2].value == 3)
    if is_ace_high_straight:
        return True, False
    return False, False


def score_sequence_and_suits(cards: list[PokerCard], counts: Counter) -> ScoreResult:
    is_straight, is_ace_low = contains_straight(cards, counts)
    is_flush = contains_flush(cards)

    if is_straight and is_flush:
        sorted_values = sorted([card.straight_value(is_ace_low) for card in cards], reverse=True)
        return PokerResult.STRAIGHT_FLUSH, sorted_values
    if is_straight:
        sorted_values = sorted([card.straight_value(is_ace_low) for card in cards], reverse=True)
        return PokerResult.STRAIGHT, sorted_values
    if is_flush:
        sorted_values = sorted([card.value for card in cards], reverse=True)
        return PokerResult.FLUSH, sorted_values


scorers = [
    score_sequence_and_suits,
    score_four_of_a_kind,
    score_full_house,
    score_three_of_a_kind,
    score_two_pair,
    score_pair,
    score_high_card,
]