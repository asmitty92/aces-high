from typing import List

import pytest
from aces_high import Card, Deck, PinochleDeck, EuchreDeck


def _get_cuts(deck: Deck) -> List[int]:
    count = 1
    cuts = []
    for i in range(1, len(deck)):
        current_card = deck[i]
        previous_card = deck[i - 1]
        if current_card.index - previous_card.index == 1:
            count += 1
        else:
            cuts.append(count)
            count = 1
    cuts.append(count)
    return cuts


@pytest.fixture
def standard_deck() -> Deck:
    return Deck()


@pytest.fixture
def pinochle_deck() -> PinochleDeck:
    return PinochleDeck()


@pytest.fixture
def euchre_deck() -> EuchreDeck:
    return EuchreDeck()


def test_standard_deck_is_created(standard_deck):
    assert len(standard_deck) == 52


def test_faro_shuffle(standard_deck: Deck):
    standard_deck.faro_shuffle()
    assert standard_deck.cards[0] == Card.create_without_value('Clubs', 'Ace')
    assert standard_deck.cards[1] == Card.create_without_value('Spades', 'Ace')
    assert standard_deck.cards[2] == Card.create_without_value('Clubs', 'Two')
    assert standard_deck.cards[3] == Card.create_without_value('Spades', 'Two')


def test_faro_shuffle_invalid_deck(standard_deck: Deck):
    with pytest.raises(ValueError):
        standard_deck.deal()
        standard_deck.faro_shuffle()


# this is a clunky test, don't love it
def test_riffle_shuffle(standard_deck: Deck):
    index = 0
    standard_deck.riffle_shuffle()
    while not standard_deck._is_empty():
        indices = [standard_deck.deal()[0].index for _ in range(2)]
        assert index in indices
        assert index + 26 in indices
        index += 1


def test_riffle_shuffle_invalid_deck(standard_deck: Deck):
    with pytest.raises(ValueError):
        standard_deck.deal()
        standard_deck.riffle_shuffle()


def test_running_cuts_shuffle(standard_deck: Deck):
    standard_deck.running_cuts_shuffle()
    cuts = _get_cuts(standard_deck)
    assert 1 <= cuts[:1][0] <= 8  # first cut is end of deck and could be smaller than a standard cut
    assert 7 <= cuts[-1:][0] <= 19  # original top of deck remains intact at between 7 and 19 cards
    for cut in cuts[1:-1]:
        assert 4 <= cut <= 8  # individual middle cuts must be between 4 and 8 cards


# Many repetitions needed to make sure it doesn't violate constraints of cut sizes
def test_running_cuts_1000_times():
    [test_running_cuts_shuffle(Deck()) for _ in range(1000)]


def test_standard_deck_has_aces(standard_deck):
    assert Card.create_without_value('Clubs', 'Ace') in standard_deck
    assert Card.create_without_value('Hearts', 'Ace') in standard_deck
    assert Card.create_without_value('Spades', 'Ace') in standard_deck
    assert Card.create_without_value('Diamonds', 'Ace') in standard_deck


def test_standard_deck_has_twos(standard_deck):
    assert Card.create_without_value('Clubs', 'Two') in standard_deck
    assert Card.create_without_value('Hearts', 'Two') in standard_deck
    assert Card.create_without_value('Spades', 'Two') in standard_deck
    assert Card.create_without_value('Diamonds', 'Two') in standard_deck


def test_standard_deck_has_threes(standard_deck):
    assert Card.create_without_value('Clubs', 'Three') in standard_deck
    assert Card.create_without_value('Hearts', 'Three') in standard_deck
    assert Card.create_without_value('Spades', 'Three') in standard_deck
    assert Card.create_without_value('Diamonds', 'Three') in standard_deck


def test_standard_deck_has_fours(standard_deck):
    assert Card.create_without_value('Clubs', 'Four') in standard_deck
    assert Card.create_without_value('Hearts', 'Four') in standard_deck
    assert Card.create_without_value('Spades', 'Four') in standard_deck
    assert Card.create_without_value('Diamonds', 'Four') in standard_deck


def test_standard_deck_has_fives(standard_deck):
    assert Card.create_without_value('Clubs', 'Five') in standard_deck
    assert Card.create_without_value('Hearts', 'Five') in standard_deck
    assert Card.create_without_value('Spades', 'Five') in standard_deck
    assert Card.create_without_value('Diamonds', 'Five') in standard_deck


def test_standard_deck_has_sixes(standard_deck):
    assert Card.create_without_value('Clubs', 'Six') in standard_deck
    assert Card.create_without_value('Hearts', 'Six') in standard_deck
    assert Card.create_without_value('Spades', 'Six') in standard_deck
    assert Card.create_without_value('Diamonds', 'Six') in standard_deck


def test_standard_deck_has_sevens(standard_deck):
    assert Card.create_without_value('Clubs', 'Seven') in standard_deck
    assert Card.create_without_value('Hearts', 'Seven') in standard_deck
    assert Card.create_without_value('Spades', 'Seven') in standard_deck
    assert Card.create_without_value('Diamonds', 'Seven') in standard_deck


def test_standard_deck_has_eights(standard_deck):
    assert Card.create_without_value('Clubs', 'Eight') in standard_deck
    assert Card.create_without_value('Hearts', 'Eight') in standard_deck
    assert Card.create_without_value('Spades', 'Eight') in standard_deck
    assert Card.create_without_value('Diamonds', 'Eight') in standard_deck


def test_standard_deck_has_nines(standard_deck):
    assert Card.create_without_value('Clubs', 'Nine') in standard_deck
    assert Card.create_without_value('Hearts', 'Nine') in standard_deck
    assert Card.create_without_value('Spades', 'Nine') in standard_deck
    assert Card.create_without_value('Diamonds', 'Nine') in standard_deck


def test_standard_deck_has_tens(standard_deck):
    assert Card.create_without_value('Clubs', 'Ten') in standard_deck
    assert Card.create_without_value('Hearts', 'Ten') in standard_deck
    assert Card.create_without_value('Spades', 'Ten') in standard_deck
    assert Card.create_without_value('Diamonds', 'Ten') in standard_deck


def test_standard_deck_has_jacks(standard_deck):
    assert Card.create_without_value('Clubs', 'Jack') in standard_deck
    assert Card.create_without_value('Hearts', 'Jack') in standard_deck
    assert Card.create_without_value('Spades', 'Jack') in standard_deck
    assert Card.create_without_value('Diamonds', 'Jack') in standard_deck


def test_standard_deck_has_queens(standard_deck):
    assert Card.create_without_value('Clubs', 'Queen') in standard_deck
    assert Card.create_without_value('Hearts', 'Queen') in standard_deck
    assert Card.create_without_value('Spades', 'Queen') in standard_deck
    assert Card.create_without_value('Diamonds', 'Queen') in standard_deck


def test_standard_deck_has_kings(standard_deck):
    assert Card.create_without_value('Clubs', 'King') in standard_deck
    assert Card.create_without_value('Hearts', 'King') in standard_deck
    assert Card.create_without_value('Spades', 'King') in standard_deck
    assert Card.create_without_value('Diamonds', 'King') in standard_deck


def test_pinochle_deck_is_created(pinochle_deck):
    assert len(pinochle_deck) == 48


def test_pinochle_deck_has_nines(pinochle_deck):
    assert len([0 for c in pinochle_deck if c.suit == 'Clubs' and c.face == 'Nine']) == 2
    assert len([0 for c in pinochle_deck if c.suit == 'Hearts' and c.face == 'Nine']) == 2
    assert len([0 for c in pinochle_deck if c.suit == 'Spades' and c.face == 'Nine']) == 2
    assert len([0 for c in pinochle_deck if c.suit == 'Diamonds' and c.face == 'Nine']) == 2


def test_pinochle_deck_has_jacks(pinochle_deck):
    assert len([0 for c in pinochle_deck if c.suit == 'Clubs' and c.face == 'Jack']) == 2
    assert len([0 for c in pinochle_deck if c.suit == 'Hearts' and c.face == 'Jack']) == 2
    assert len([0 for c in pinochle_deck if c.suit == 'Spades' and c.face == 'Jack']) == 2
    assert len([0 for c in pinochle_deck if c.suit == 'Diamonds' and c.face == 'Jack']) == 2


def test_pinochle_deck_has_queens(pinochle_deck):
    assert len([0 for c in pinochle_deck if c.suit == 'Clubs' and c.face == 'Queen']) == 2
    assert len([0 for c in pinochle_deck if c.suit == 'Hearts' and c.face == 'Queen']) == 2
    assert len([0 for c in pinochle_deck if c.suit == 'Spades' and c.face == 'Queen']) == 2
    assert len([0 for c in pinochle_deck if c.suit == 'Diamonds' and c.face == 'Queen']) == 2


def test_pinochle_deck_has_kings(pinochle_deck):
    assert len([0 for c in pinochle_deck if c.suit == 'Clubs' and c.face == 'King']) == 2
    assert len([0 for c in pinochle_deck if c.suit == 'Hearts' and c.face == 'King']) == 2
    assert len([0 for c in pinochle_deck if c.suit == 'Spades' and c.face == 'King']) == 2
    assert len([0 for c in pinochle_deck if c.suit == 'Diamonds' and c.face == 'King']) == 2


def test_pinochle_deck_has_tens(pinochle_deck):
    assert len([0 for c in pinochle_deck if c.suit == 'Clubs' and c.face == 'Ten']) == 2
    assert len([0 for c in pinochle_deck if c.suit == 'Hearts' and c.face == 'Ten']) == 2
    assert len([0 for c in pinochle_deck if c.suit == 'Spades' and c.face == 'Ten']) == 2
    assert len([0 for c in pinochle_deck if c.suit == 'Diamonds' and c.face == 'Ten']) == 2


def test_pinochle_deck_has_aces(pinochle_deck):
    assert len([0 for c in pinochle_deck if c.suit == 'Clubs' and c.face == 'Ace']) == 2
    assert len([0 for c in pinochle_deck if c.suit == 'Hearts' and c.face == 'Ace']) == 2
    assert len([0 for c in pinochle_deck if c.suit == 'Spades' and c.face == 'Ace']) == 2
    assert len([0 for c in pinochle_deck if c.suit == 'Diamonds' and c.face == 'Ace']) == 2


def test_pinochle_deck_deals_three(pinochle_deck):
    assert len(pinochle_deck.deal()) == 3
    assert len(pinochle_deck.deal()) == 3


def test_euchre_deck_is_created(euchre_deck):
    assert len(euchre_deck) == 24


def test_euchre_deck_has_nines(euchre_deck):
    assert Card.create_without_value('Clubs', 'Nine') in euchre_deck
    assert Card.create_without_value('Hearts', 'Nine') in euchre_deck
    assert Card.create_without_value('Spades', 'Nine') in euchre_deck
    assert Card.create_without_value('Diamonds', 'Nine') in euchre_deck


def test_euchre_deck_has_tens(euchre_deck):
    assert Card.create_without_value('Clubs', 'Ten') in euchre_deck
    assert Card.create_without_value('Hearts', 'Ten') in euchre_deck
    assert Card.create_without_value('Spades', 'Ten') in euchre_deck
    assert Card.create_without_value('Diamonds', 'Ten') in euchre_deck


def test_euchre_deck_has_jacks(euchre_deck):
    assert Card.create_without_value('Clubs', 'Jack') in euchre_deck
    assert Card.create_without_value('Hearts', 'Jack') in euchre_deck
    assert Card.create_without_value('Spades', 'Jack') in euchre_deck
    assert Card.create_without_value('Diamonds', 'Jack') in euchre_deck


def test_euchre_deck_has_queens(euchre_deck):
    assert Card.create_without_value('Clubs', 'Queen') in euchre_deck
    assert Card.create_without_value('Hearts', 'Queen') in euchre_deck
    assert Card.create_without_value('Spades', 'Queen') in euchre_deck
    assert Card.create_without_value('Diamonds', 'Queen') in euchre_deck


def test_euchre_deck_has_kings(euchre_deck):
    assert Card.create_without_value('Clubs', 'King') in euchre_deck
    assert Card.create_without_value('Hearts', 'King') in euchre_deck
    assert Card.create_without_value('Spades', 'King') in euchre_deck
    assert Card.create_without_value('Diamonds', 'King') in euchre_deck


def test_euchre_deck_has_aces(euchre_deck):
    assert Card.create_without_value('Clubs', 'Ace') in euchre_deck
    assert Card.create_without_value('Hearts', 'Ace') in euchre_deck
    assert Card.create_without_value('Spades', 'Ace') in euchre_deck
    assert Card.create_without_value('Diamonds', 'Ace') in euchre_deck


def test_euchre_deck_alternating_deal(euchre_deck):
    assert len(euchre_deck.deal()) == 3
    assert len(euchre_deck.deal()) == 2
    assert len(euchre_deck.deal()) == 3
    assert len(euchre_deck.deal()) == 2
