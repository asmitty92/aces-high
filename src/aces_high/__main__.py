import os
from itertools import combinations
from random import randrange

import click
from stopwatch import StopWatch

from .cribtools import choose_best_cribbage_hand_with_score
from .deck import Deck
from .scorers import score_cribbage_hand, score_poker_hand, PokerHands, find_best_poker_hand, get_combinations, \
    get_combinations_v2, get_v3

poker_probabilities = {
    'HIGH_CARD': '50.1177%',
    'PAIR': '42.2569%',
    'TWO_PAIR': '4.7539%',
    'THREE_OF_A_KIND': '2.1128%',
    'STRAIGHT': '0.3925%',
    'FLUSH': '0.1965%',
    'FULL_HOUSE': '0.1441%',
    'FOUR_OF_A_KIND': '0.02401%',
    'STRAIGHT_FLUSH': '0.00139%',
    'ROYAL_FLUSH': '0.000154%'
}

poker_7_probabilities = {
    'HIGH_CARD': '17.4%',
    'PAIR': '43.8%',
    'TWO_PAIR': '23.5%',
    'THREE_OF_A_KIND': '4.83%',
    'STRAIGHT': '4.62%',
    'FLUSH': '3.03%',
    'FULL_HOUSE': '2.60%',
    'FOUR_OF_A_KIND': '0.168%',
    'STRAIGHT_FLUSH': '0.0311%',
    'ROYAL_FLUSH': '0.0032%'
}


def create_data_directory():
    if not os.path.exists('data'):
        os.mkdir('data')


def cribbage_tests(max_iterations):
    scores = {i: 0 for i in range(0, 30)}
    stopwatch = StopWatch()

    with stopwatch:
        deck = Deck().full_shuffle()
        for i in range(0, max_iterations):
            cards = [deck.deal() for _ in range(6)]
            card = deck.deal()

            hand, pre_turn_score = choose_best_cribbage_hand_with_score(cards)
            score = score_cribbage_hand(hand, card)

            scores[score] += 1

            if score in [28, 29]:
                print(f'Found a 29-point hand at {i}')

            if i % 10000 == 0:
                print(i)

            cards.append(card)
            deck.return_cards(cards)
            deck \
                .riffle_shuffle()

        [print(f'{key}: {value}: {(value / (max_iterations * 1.0)) * 100:.2f}') for key, value in scores.items() if
         value > 0]


def crib_collect(max_iterations):
    with open('data/cribbage_hands.txt', 'a') as file:
        for _ in range(max_iterations):
            deck = Deck().full_shuffle()
            full_hand = [deck.deal() for _ in range(6)]
            crib_hand, pre_cut_score = choose_best_cribbage_hand_with_score(full_hand)
            passed_to_crib = [card for card in full_hand if card not in crib_hand]
            cut_card = deck[randrange(len(deck))]
            score = score_cribbage_hand(crib_hand, cut_card)

            file.write('{}|{}|{}|{}|{}|{}\n'.format(
                full_hand,
                crib_hand,
                cut_card,
                passed_to_crib,
                pre_cut_score,
                score
            ))


def calculate_percentage(value, max_iterations):
    return f'{((value / (max_iterations * 1.0)) * 100):.6f}%'


def poker_tests(max_iterations):
    results = {hand_type: 0 for hand_type in PokerHands.get_all()}

    with StopWatch():
        deck = Deck().full_shuffle()
        for _ in range(max_iterations):
            primary_hand = []
            other_cards = []
            for _ in range(5):
                primary_hand += deck.deal()
                other_cards += deck.deal(4)
            score = score_poker_hand(primary_hand)
            hand_type = PokerHands.get_by_value(score)
            results[hand_type] += 1

            deck.return_cards(primary_hand + other_cards)
            deck.riffle_shuffle()

    print('Hand Value          : Count     : Percent     : Probability')
    [print(f'{key.ljust(20)}: {str(value).ljust(10)}: {calculate_percentage(value, max_iterations).ljust(12)}'
           f': {poker_probabilities[key].ljust(10)}')
     for key, value in results.items()]


def poker_7_tests(max_iterations):
    results = {hand_type: 0 for hand_type in PokerHands.get_all()}

    with StopWatch():
        deck = Deck().full_shuffle()
        for _ in range(max_iterations):
            primary_hand = []
            other_cards = []
            for _ in range(7):
                primary_hand += deck.deal()
                other_cards += deck.deal(4)

            hand, score = find_best_poker_hand(primary_hand)
            hand_type = PokerHands.get_by_value(score)
            results[hand_type] += 1

            deck.return_cards(primary_hand + other_cards)
            deck.riffle_shuffle()

    print('Hand Value          : Count     : Percent     : Probability')
    [print(f'{key.ljust(20)}: {str(value).ljust(10)}: {calculate_percentage(value, max_iterations).ljust(12)}'
           f': {poker_7_probabilities[key].ljust(10)}')
     for key, value in results.items()]


test_functions = {
    'cribbage': cribbage_tests,
    'crib_collect': crib_collect,
    'poker': poker_tests,
    'poker_7': poker_7_tests
}


@click.command()
@click.option('-md', '--mode', required=True, type=str)
@click.option('-max', '--max_iterations', required=False, type=int)
def run_process(mode, max_iterations):
    try:
        max_iterations = 10000 if max_iterations is None else max_iterations
        test_function = test_functions[mode]
        test_function(max_iterations)
    except KeyError:
        raise ValueError('Invalid mode provided')


if __name__ == '__main__':
    # run_process()
    items = [i for i in range(10000)]
    count = 2
    # with StopWatch():
    #     print(len(get_combinations(items, count)))
    # with StopWatch():
    #     print(len(get_combinations_v2(items, count)))
    # with StopWatch():
    #     print(len(get_v3(items)))
    with StopWatch():
        print(len(list(combinations(items, count))))
