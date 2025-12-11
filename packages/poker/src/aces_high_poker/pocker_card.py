from aces_high_core import Card, Rank


class PokerCard:
    def __init__(self, card: Card):
        self.card = card

    def __repr__(self):
        return repr(self.card)

    def __eq__(self, other):
        return self.card == other.card

    @property
    def value(self):
        return 14 if self.card.value == 1 else self.card.value

    @property
    def rank(self):
        return self.card.rank

    @property
    def suit(self):
        return self.card.suit

    def straight_value(self, is_ace_low: bool):
        if is_ace_low and self.rank == Rank.ACE:
            return 1
        return self.value