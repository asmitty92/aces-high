from collections import Counter

from aces_high_core import Card, Rank

from .scorers import scorers, ScoreResult
from .pocker_card import PokerCard


class PokerHand:
    def __init__(self, cards: list[Card]):
        if len(cards) != 5:
            raise ValueError("must contain exactly 5 cards")
        self.cards = [PokerCard(card) for card in cards]

    def __repr__(self):
        return ", ".join(str(card) for card in self.cards)

    def __len__(self):
        return len(self.cards)

    def calculate_score(self) -> ScoreResult:
        counts = Counter(card.rank for card in self.cards)
        for scorer in scorers:
            result = scorer(self.cards, counts)
            if result is not None:
                return result
        raise ValueError("No valid hand pattern matched")

    def _rank_frequencies(self) -> dict[Rank, int]:
        return Counter(card.rank for card in self.cards)


class PokerPlayer:
    def __init__(self, name):
        self.name = name
        self.hand = None
        self.score = 0
        self.hands = None
        self.hand_values = None

    def __repr__(self):
        return f"{self.name}: [{self.hand}]" if self.hand else f"{self.name}: (no hand)"

    def accept_cards(self, cards: list[Card]):
        self.hand = PokerHand(cards)

    def score_hand(self):
        self.score, self.hand_values = self.hand.calculate_score()
