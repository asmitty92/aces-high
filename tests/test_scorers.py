from aces_high import Card, score_cribbage_hand, find_best_poker_hand
from aces_high import score_poker_hand, PokerHands


def test_score_cribbage_hand_given_29_points():
    cards = [Card('Hearts', 'Five', 5), Card('Clubs', 'Five', 5), Card('Spades', 'Five', 5),
             Card('Diamonds', 'Jack', 11)]
    turn_card = Card('Diamonds', 'Five', 5)
    score = score_cribbage_hand(cards, turn_card, False)
    assert score == 29


def test_score_cribbage_hand_given_28_points():
    cards = [Card('Hearts', 'Five', 5), Card('Clubs', 'Five', 5), Card('Spades', 'Five', 5),
             Card('Hearts', 'Ten', 10)]
    turn_card = Card('Diamonds', 'Five', 5)
    score = score_cribbage_hand(cards, turn_card, False)
    assert score == 28


def test_score_cribbage_hand_given_1_set():
    cards = [Card('Clubs', 'Eight', 8), Card('Clubs', 'Queen', 12), Card('Spades', 'Eight', 8), Card('Clubs', 'Two', 2)]
    turn_card = Card('Hearts', 'King', 13)
    score = score_cribbage_hand(cards, turn_card, False)
    assert score == 2


def test_score_cribbage_hand_given_one_fifteen():
    cards = [Card('Clubs', 'Eight', 8), Card('Clubs', 'Seven', 7), Card('Spades', 'Ten', 10), Card('Clubs', 'Two', 2)]
    turn_card = Card('Hearts', 'King', 13)
    score = score_cribbage_hand(cards, turn_card, False)
    assert score == 2


def test_score_cribbage_hand_given_15_2_4_and_a_pair_for_six():
    cards = [Card('Clubs', 'Seven', 7), Card('Spades', 'Seven', 7), Card('Clubs', 'Eight', 8), Card('Clubs', 'Two', 2)]
    turn_card = Card('Hearts', 'King', 13)
    score = score_cribbage_hand(cards, turn_card, False)
    assert score == 6


def test_score_cribbage_hand_given_straight_eight():
    cards = [Card('Clubs', 'Three', 3), Card('Hearts', 'Four', 4), Card('Spades', 'Four', 4), Card('Clubs', 'Five', 5)]
    turn_card = Card('Diamonds', 'Ace', 1)
    score = score_cribbage_hand(cards, turn_card, False)
    assert score == 8


def test_score_cribbage_hand_given_4_card_flush_not_crib():
    cards = [Card('Spades', 'Two', 2), Card('Spades', 'Four', 4), Card('Spades', 'Six', 6), Card('Spades', 'Eight', 8)]
    turn_card = Card('Hearts', 'Ten', 10)
    score = score_cribbage_hand(cards, turn_card, False)
    assert score == 4


def test_score_cribbage_hand_given_4_card_flush_in_crib():
    cards = [Card('Spades', 'Four', 4), Card('Spades', 'Two', 2), Card('Spades', 'Eight', 8), Card('Spades', 'Six', 6)]
    turn_card = Card('Hearts', 'Ten', 10)
    score = score_cribbage_hand(cards, turn_card, True)
    assert score == 0


def test_score_cribbage_hand_given_5_card_flush_not_crib():
    cards = [Card('Spades', 'Four', 4), Card('Spades', 'Six', 6), Card('Spades', 'Two', 2), Card('Spades', 'Eight', 8)]
    turn_card = Card('Spades', 'Ten', 10)
    score = score_cribbage_hand(cards, turn_card, False)
    assert score == 5


def test_score_cribbage_hand_given_5_card_flush_in_crib():
    cards = [Card('Spades', 'Two', 2), Card('Spades', 'Eight', 8), Card('Spades', 'Four', 4), Card('Spades', 'Six', 6)]
    turn_card = Card('Spades', 'Ten', 10)
    score = score_cribbage_hand(cards, turn_card, True)
    assert score == 5


def test_score_cribbage_hand_given_his_nobs():
    cards = [Card('Hearts', 'Two', 2), Card('Clubs', 'Eight', 8), Card('Diamonds', 'Four', 4),
             Card('Spades', 'Jack', 11)]
    turn_card = Card('Spades', 'Ten', 10)
    score = score_cribbage_hand(cards, turn_card, True)
    assert score == 1


def test_score_cribbage_hand_given_3_card_run():
    cards = [Card('Clubs', 'Jack', 11), Card('Hearts', 'Four', 4), Card('Spades', 'Queen', 12), Card('Clubs', 'Ten', 10)]
    turn_card = Card('Diamonds', 'Two', 2)
    score = score_cribbage_hand(cards, turn_card, False)
    assert score == 3


def test_score_cribbage_hand_given_4_card_run():
    cards = [Card('Clubs', 'Jack', 11), Card('Hearts', 'Queen', 12), Card('Spades', 'King', 13),
             Card('Clubs', 'Ten', 10)]
    turn_card = Card('Diamonds', 'Ace', 1)
    score = score_cribbage_hand(cards, turn_card, False)
    assert score == 4


def test_score_cribbage_hand_given_5_card_run():
    cards = [Card('Clubs', 'Nine', 9), Card('Hearts', 'Queen', 12), Card('Spades', 'King', 13), Card('Clubs', 'Ten', 10)]
    turn_card = Card('Diamonds', 'Jack', 11)
    score = score_cribbage_hand(cards, turn_card, False)
    assert score == 5


def test_score_poker_hand_given_high_card():
    cards = [Card('Hearts', 'Five', 5), Card('Hearts', 'Six', 6), Card('Clubs', 'Eight', 8),
             Card('Diamonds', 'Queen', 12), Card('Spades', 'Two', 2)]
    score = score_poker_hand(cards)
    assert score == PokerHands.HIGH_CARD


def test_score_poker_hand_given_pair():
    cards = [Card('Hearts', 'Five', 5), Card('Clubs', 'Five', 5), Card('Clubs', 'Eight', 8),
             Card('Diamonds', 'Queen', 12), Card('Spades', 'Two', 2)]
    score = score_poker_hand(cards)
    assert score == PokerHands.PAIR


def test_score_poker_hand_given_two_pair():
    cards = [Card('Hearts', 'Five', 5), Card('Clubs', 'Five', 5), Card('Clubs', 'Eight', 8),
             Card('Diamonds', 'Eight', 8), Card('Spades', 'Two', 2)]
    score = score_poker_hand(cards)
    assert score == PokerHands.TWO_PAIR


def test_score_poker_hand_given_three_of_a_kind():
    cards = [Card('Hearts', 'Five', 5), Card('Clubs', 'Five', 5), Card('Clubs', 'Eight', 8),
             Card('Diamonds', 'Queen', 12), Card('Spades', 'Five', 5)]
    score = score_poker_hand(cards)
    assert score == PokerHands.THREE_OF_A_KIND


def test_score_poker_hand_given_straight():
    cards = [Card('Hearts', 'Five', 5), Card('Hearts', 'Four', 4), Card('Clubs', 'Eight', 8),
             Card('Diamonds', 'Seven', 7), Card('Spades', 'Six', 6)]
    score = score_poker_hand(cards)
    assert score == PokerHands.STRAIGHT


def test_score_poker_hand_given_straight_with_ace_high():
    cards = [Card('Hearts', 'Queen', 12), Card('Hearts', 'Ten', 10), Card('Clubs', 'King', 13),
             Card('Diamonds', 'Ace', 1), Card('Spades', 'Jack', 11)]
    score = score_poker_hand(cards)
    assert score == PokerHands.STRAIGHT


def test_score_poker_hand_flush():
    cards = [Card('Hearts', 'Five', 5), Card('Hearts', 'Ace', 1), Card('Hearts', 'Eight', 8),
             Card('Hearts', 'Queen', 12), Card('Hearts', 'Two', 2)]
    score = score_poker_hand(cards)
    assert score == PokerHands.FLUSH


def test_score_poker_hand_given_3_high_full_house():
    cards = [Card('Hearts', 'Five', 5), Card('Spades', 'Five', 5), Card('Clubs', 'Five', 5),
             Card('Diamonds', 'Two', 2), Card('Spades', 'Two', 2)]
    score = score_poker_hand(cards)
    assert score == PokerHands.FULL_HOUSE


def test_score_poker_hand_given_3_low_full_house():
    cards = [Card('Hearts', 'Five', 5), Card('Spades', 'Five', 5), Card('Clubs', 'Two', 2),
             Card('Diamonds', 'Two', 2), Card('Spades', 'Two', 2)]
    score = score_poker_hand(cards)
    assert score == PokerHands.FULL_HOUSE


def test_score_poker_hand_given_four_of_a_kind():
    cards = [Card('Hearts', 'Two', 2), Card('Spades', 'Five', 5), Card('Clubs', 'Two', 2),
             Card('Diamonds', 'Two', 2), Card('Spades', 'Two', 2)]
    score = score_poker_hand(cards)
    assert score == PokerHands.FOUR_OF_A_KIND


def test_score_poker_hand_given_straight_flush():
    cards = [Card('Hearts', 'Five', 5), Card('Hearts', 'Four', 4), Card('Hearts', 'Eight', 8),
             Card('Hearts', 'Seven', 7), Card('Hearts', 'Six', 6)]
    score = score_poker_hand(cards)
    assert score == PokerHands.STRAIGHT_FLUSH


def test_score_poker_hand_given_royal_flush():
    cards = [Card('Hearts', 'Queen', 12), Card('Hearts', 'Ten', 10), Card('Hearts', 'King', 13),
             Card('Hearts', 'Ace', 1), Card('Hearts', 'Jack', 11)]
    score = score_poker_hand(cards)
    assert score == PokerHands.ROYAL_FLUSH


def test_find_best_poker_hand_given_full_house_and_four_of_a_kind():
    cards = [Card('Hearts', 'Two', 2), Card('Spades', 'Five', 5), Card('Clubs', 'Two', 2),
             Card('Diamonds', 'Two', 2), Card('Spades', 'Two', 2), Card('Clubs', 'Five', 5),
             Card('Diamonds', 'Ace', 1)]
    hand, score = find_best_poker_hand(cards)
    assert score == PokerHands.FOUR_OF_A_KIND
