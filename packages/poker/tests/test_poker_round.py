import pytest

from aces_high_poker import PokerPlayer, PokerRound


@pytest.fixture
def players():
    return [PokerPlayer("Bob"), PokerPlayer("Alice")]


@pytest.fixture
def poker_round(players):
    return PokerRound(players)


def test_poker_round_has_players(players, poker_round):
    assert poker_round.players == players


def test_poker_round_has_deck(poker_round):
    assert poker_round.deck is not None


def test_poker_round_has_empty_scores_collection(poker_round):
    assert poker_round.scores == {}


def test_poker_round_has_empty_winners_list(poker_round):
    assert poker_round.winners == []


def test_poker_round_deals_hands(poker_round):
    poker_round.deal_hands()
    assert len(poker_round.players[0].hand) == 5
    assert len(poker_round.players[1].hand) == 5


