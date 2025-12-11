from aces_high_core import StandardDeck

from .poker_player import PokerPlayer
from .scorers import ScoreResult


class PokerRound:
    def __init__(self, players: list[PokerPlayer]):
        self.players = players
        self.deck = StandardDeck()
        self.scores: dict[PokerPlayer, ScoreResult] = {}
        self.winners: list[PokerPlayer] = []

        self.deck.shuffle()

    def deal_hands(self):
        for player in self.players:
            player.accept_cards(self.deck.deal(5))


