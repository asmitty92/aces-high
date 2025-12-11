import random
from typing import List

from .cardtools import coin_flip


class Card:
    def __init__(self, suit, face, value, index=-1):
        self.face = face
        self.suit = suit
        self.value = value
        self.index = index

    def __repr__(self):
        return f'Card(suit={self.suit}, face={self.face}, value={self.value}, index={self.index})'

    def __str__(self):
        return f"The {self.face} of {self.suit}"

    def __eq__(self, other):
        return self.face == other.face and self.suit == other.suit

    def is_in_deck(self):
        return self.index >= 0

    def is_ace(self):
        return self.value == 1

    def is_king(self):
        return self.value == 13

    @classmethod
    def create_without_value(cls, suit, face):
        return cls(suit, face, -1)


class Deck:
    """
    This class represents a standard deck of 52 cards
    """
    SUITS = ("Clubs", "Hearts", "Spades", "Diamonds")
    FACES = ("Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King")

    def __init__(self):
        self.cards = self._create_cards(self.SUITS, self.FACES)

    def __iter__(self):
        return iter(self.cards)

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return '{}(cards=[\n\t{}\n])'.format(
            type(self).__name__,
            ", \n\t".join([repr(card) for card in self.cards])
        )
        # return f'{type(self).__name__}(cards=[\n{", ".join([repr(card) for card in self.cards])}])'

    def __str__(self):
        return '\n'.join([str(card) for card in self.cards])

    def __getitem__(self, index):
        return self.cards[index]

    @staticmethod
    def _create_cards(suits, faces):
        index = 0
        cards = []
        for s in suits:
            for v, f in enumerate(faces):
                cards.append(Card(s, f, v + 1, index))
                index += 1
        return cards

    def full_shuffle(self):
        """
            This mimics a full human shuffle with the following steps:
            1 random_shuffle()
            3 riffle_shuffle()
            1 running_cuts_shuffle()
            3 riffle_shuffle()
            1 running_cuts_shuffle()
        """
        self.random_shuffle()

        for _ in range(0, 3):
            self.riffle_shuffle()

        self.running_cuts_shuffle()

        for _ in range(0, 3):
            self.riffle_shuffle()

        self.running_cuts_shuffle()

        return self

    def random_shuffle(self):
        """
        This method randomizes a new deck from 'perfect numerical order' to something other than that.
        It uses a pseudorandom number generator to swap each card with a different position in the deck.
        :return: a deck for method chaining
        """
        for i in range(0, len(self.cards)):
            index = random.randint(0, len(self.cards) - 1)
            self.cards[i], self.cards[index] = self.cards[index], self.cards[i]
        return self

    def riffle_shuffle(self):
        """
        This method mimics a human riffle shuffle. It randomizes whether the card
        :return:
        """
        top, bottom = self._split_deck()

        self.cards = []
        for i in range(0, len(top)):
            flip = coin_flip()
            if flip == 0:
                self.cards.append(top[i])
                self.cards.append(bottom[i])
            else:
                self.cards.append(bottom[i])
                self.cards.append(top[i])

        return self

    def running_cuts_shuffle(self):
        if len(self.cards) % 4 != 0:
            raise ValueError('Only a full deck can be shuffled')

        cut_sizes = [4, 5, 6, 7, 8]
        quarter = int(len(self.cards) / 4)
        half_quarter = int(quarter / 2)
        cut_start = quarter + random.randint(-1 * half_quarter, half_quarter)

        to_cut = self.cards[cut_start:]
        self.cards = self.cards[:cut_start]

        while len(to_cut) > 0:
            cut_index = random.randint(0, len(cut_sizes) - 1)
            cut_size = cut_sizes[cut_index]
            self.cards = to_cut[:cut_size] + self.cards
            to_cut = to_cut[cut_size:]

        return self

    def faro_shuffle(self):
        top, bottom = self._split_deck()

        self.cards = []
        for i in range(len(top)):
            self.cards.append(top[i])
            self.cards.append(bottom[i])

    def reorder(self):
        self.cards.sort(key=lambda card: card.index)
        return self

    def deal(self, card_count: int = 1) -> List[Card]:
        if self._is_empty():
            raise StopIteration()
        cards = self.cards[:1]
        self.cards = self.cards[1:]
        return cards

    def take_card(self, index):
        pass

    def return_cards(self, cards):
        index = random.randint(0, len(self.cards) - 1)
        self.cards = self.cards[:index] + cards + self.cards[index:]

    def _is_empty(self):
        return len(self.cards) <= 0

    def _split_deck(self, number_of_parts=2):
        if len(self.cards) % 2 != 0:
            raise ValueError('Only a full deck can be shuffled')

        mid = int(len(self.cards) / 2)

        return self.cards[:mid], self.cards[mid:]


class PinochleDeck(Deck):
    """This class handles a specialized deck of 48 cards for the game of Pinochle"""
    FACES = ("Nine", "Nine", "Jack", "Jack", "Queen", "Queen", "King", "King", "Ten", "Ten", "Ace", "Ace")

    def __init__(self):
        super().__init__()

    def deal(self):
        return [super(PinochleDeck, self).deal() for _ in range(3)]


class EuchreDeck(Deck):
    """This class handles a specialized deck of 24 cards for the game of Euchre"""
    FACES = ("Nine", "Ten", "Jack", "Queen", "King", "Ace")

    def __init__(self):
        super().__init__()
        self._last_deal_count = 2  # always start with last deal count of 2 to start with 3

    def deal(self):
        if self._last_deal_count == 2:
            self._last_deal_count = 3
            return [super(EuchreDeck, self).deal() for _ in range(3)]
        else:
            self._last_deal_count = 2
            return [super(EuchreDeck, self).deal() for _ in range(2)]
