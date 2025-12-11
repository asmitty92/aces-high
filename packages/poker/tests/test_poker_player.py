import pytest
from aces_high_core import Card, Suit, Rank

from aces_high_poker import PokerPlayer, PokerHand, PokerResult
from aces_high_poker.poker_player import PokerCard


@pytest.fixture
def poker_player():
    return PokerPlayer(name="Bob")


def test_player_initial_state():
    player = PokerPlayer(name="Alice")
    assert player.name == "Alice"
    assert player.hand is None
    

def test_player_can_accept_cards():
    cards = [Card(Suit.SPADES, Rank.TEN), Card(Suit.HEARTS, Rank.JACK),
             Card(Suit.CLUBS, Rank.QUEEN), Card(Suit.DIAMONDS, Rank.KING),
             Card(Suit.SPADES, Rank.ACE)]
    player = PokerPlayer(name="Bob")
    player.accept_cards(cards)

    assert player.hand is not None
    assert isinstance(player.hand, PokerHand)
    assert player.hand.cards == [PokerCard(card) for card in cards]


def test_poker_hand_rejects_too_many_cards():
    cards = [Card(Suit.SPADES, Rank.TEN)] * 6
    with pytest.raises(ValueError, match="must contain exactly 5 cards"):
        PokerHand(cards)


def test_poker_hand_rejects_too_few_cards():
    cards = [Card(Suit.SPADES, Rank.TEN)] * 4
    with pytest.raises(ValueError, match="must contain exactly 5 cards"):
        PokerHand(cards)


def test_poker_hand_scores_high_card(poker_player):
    cards = [
        Card(Suit.CLUBS, Rank.ACE),
        Card(Suit.HEARTS, Rank.THREE),
        Card(Suit.CLUBS, Rank.EIGHT),
        Card(Suit.CLUBS, Rank.SIX),
        Card(Suit.CLUBS, Rank.FOUR),
    ]
    poker_player.accept_cards(cards)

    poker_player.score_hand()

    assert poker_player.score == PokerResult.HIGH_CARD
    assert poker_player.hand_values == [14, 8, 6, 4, 3]


def test_poker_hand_scores_pair(poker_player):
    cards = [
        Card(Suit.CLUBS, Rank.TWO),
        Card(Suit.CLUBS, Rank.FOUR),
        Card(Suit.HEARTS, Rank.FOUR),
        Card(Suit.CLUBS, Rank.NINE),
        Card(Suit.CLUBS, Rank.JACK),
    ]
    poker_player.accept_cards(cards)

    poker_player.score_hand()

    assert poker_player.score == PokerResult.PAIR
    assert poker_player.hand_values == [4, 11, 9, 2]


def test_poker_hand_scores_two_pairs(poker_player):
    cards = [
        Card(Suit.CLUBS, Rank.TWO),
        Card(Suit.CLUBS, Rank.FOUR),
        Card(Suit.HEARTS, Rank.FOUR),
        Card(Suit.SPADES, Rank.NINE),
        Card(Suit.DIAMONDS, Rank.NINE),
    ]
    poker_player.accept_cards(cards)

    poker_player.score_hand()

    assert poker_player.score == PokerResult.TWO_PAIR
    assert poker_player.hand_values == [9, 4, 2]


def test_poker_hand_scores_three_of_a_kind(poker_player):
    cards = [
        Card(Suit.CLUBS, Rank.FOUR),
        Card(Suit.HEARTS, Rank.NINE),
        Card(Suit.SPADES, Rank.NINE),
        Card(Suit.CLUBS, Rank.NINE),
        Card(Suit.CLUBS, Rank.TWO),
    ]
    poker_player.accept_cards(cards)

    poker_player.score_hand()

    assert poker_player.score == PokerResult.THREE_OF_A_KIND
    assert poker_player.hand_values == [9, 4, 2]


def test_poker_hand_scores_full_house(poker_player):
    cards = [
        Card(Suit.DIAMONDS, Rank.ACE),
        Card(Suit.CLUBS, Rank.NINE),
        Card(Suit.HEARTS, Rank.ACE),
        Card(Suit.HEARTS, Rank.NINE),
        Card(Suit.SPADES, Rank.NINE),
    ]
    poker_player.accept_cards(cards)

    poker_player.score_hand()

    assert poker_player.score == PokerResult.FULL_HOUSE
    assert poker_player.hand_values == [9, 14]


def test_poker_hand_scores_four_of_a_kind(poker_player):
    cards = [
        Card(Suit.CLUBS, Rank.KING),
        Card(Suit.DIAMONDS, Rank.FOUR),
        Card(Suit.CLUBS, Rank.FOUR),
        Card(Suit.SPADES, Rank.FOUR),
        Card(Suit.HEARTS, Rank.FOUR),
    ]
    poker_player.accept_cards(cards)

    poker_player.score_hand()

    assert poker_player.score == PokerResult.FOUR_OF_A_KIND
    assert poker_player.hand_values == [4, 13]


def test_poker_hand_scores_straight(poker_player):
    cards = [
        Card(Suit.DIAMONDS, Rank.TWO),
        Card(Suit.CLUBS, Rank.FOUR),
        Card(Suit.SPADES, Rank.THREE),
        Card(Suit.DIAMONDS, Rank.SIX),
        Card(Suit.SPADES, Rank.FIVE),
    ]
    poker_player.accept_cards(cards)

    poker_player.score_hand()

    assert poker_player.score == PokerResult.STRAIGHT
    assert poker_player.hand_values == [6, 5, 4, 3, 2]


def test_poker_hand_scores_ace_low_straight(poker_player):
    cards = [
        Card(Suit.DIAMONDS, Rank.TWO),
        Card(Suit.CLUBS, Rank.FOUR),
        Card(Suit.SPADES, Rank.THREE),
        Card(Suit.DIAMONDS, Rank.ACE),
        Card(Suit.SPADES, Rank.FIVE),
    ]
    poker_player.accept_cards(cards)

    poker_player.score_hand()

    assert poker_player.score == PokerResult.STRAIGHT
    assert poker_player.hand_values == [5, 4, 3, 2, 1]


def test_poker_hand_scores_ace_high_straight(poker_player):
    cards = [
        Card(Suit.DIAMONDS, Rank.JACK),
        Card(Suit.CLUBS, Rank.QUEEN),
        Card(Suit.CLUBS, Rank.TEN),
        Card(Suit.SPADES, Rank.ACE),
        Card(Suit.DIAMONDS, Rank.KING),
    ]
    poker_player.accept_cards(cards)

    poker_player.score_hand()

    assert poker_player.score == PokerResult.STRAIGHT
    assert poker_player.hand_values == [14, 13, 12, 11, 10]


def test_poker_hand_scores_flush(poker_player):
    cards = [
        Card(Suit.CLUBS, Rank.KING),
        Card(Suit.CLUBS, Rank.FIVE),
        Card(Suit.CLUBS, Rank.THREE),
        Card(Suit.CLUBS, Rank.EIGHT),
        Card(Suit.CLUBS, Rank.NINE),
    ]
    poker_player.accept_cards(cards)

    poker_player.score_hand()

    assert poker_player.score == PokerResult.FLUSH
    assert poker_player.hand_values == [13, 9, 8, 5, 3]


def test_poker_hand_scores_straight_flush(poker_player):
    cards = [
        Card(Suit.DIAMONDS, Rank.NINE),
        Card(Suit.DIAMONDS, Rank.JACK),
        Card(Suit.DIAMONDS, Rank.KING),
        Card(Suit.DIAMONDS, Rank.QUEEN),
        Card(Suit.DIAMONDS, Rank.TEN),
    ]
    poker_player.accept_cards(cards)

    poker_player.score_hand()

    assert poker_player.score == PokerResult.STRAIGHT_FLUSH
    assert poker_player.hand_values == [13, 12, 11, 10, 9]


def test_poker_hand_scores_ace_high_straight_flush(poker_player):
    cards = [
        Card(Suit.DIAMONDS, Rank.ACE),
        Card(Suit.DIAMONDS, Rank.JACK),
        Card(Suit.DIAMONDS, Rank.KING),
        Card(Suit.DIAMONDS, Rank.QUEEN),
        Card(Suit.DIAMONDS, Rank.TEN),
    ]
    poker_player.accept_cards(cards)

    poker_player.score_hand()

    assert poker_player.score == PokerResult.STRAIGHT_FLUSH
    assert poker_player.hand_values == [14, 13, 12, 11, 10]


def test_poker_hand_scores_ace_low_straight_flush(poker_player):
    cards = [
        Card(Suit.SPADES, Rank.TWO),
        Card(Suit.SPADES, Rank.FOUR),
        Card(Suit.SPADES, Rank.THREE),
        Card(Suit.SPADES, Rank.ACE),
        Card(Suit.SPADES, Rank.FIVE),
    ]
    poker_player.accept_cards(cards)

    poker_player.score_hand()

    assert poker_player.score == PokerResult.STRAIGHT_FLUSH
    assert poker_player.hand_values == [5, 4, 3, 2, 1]