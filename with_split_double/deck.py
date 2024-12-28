import random
from card import Card
"""
Represents a standard deck of playing cards in blackjack. Has attributes and 
methods that allows for storing values of cards as well as drawing cards at r
andom without replacement. 

Attributes:
  _cards (list): A list containing all playing cards in blackjack. 
"""


class Deck:
    ranks = [('Ace', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6),
             ('7', 7), ('8', 8), ('9', 9), ('10', 10), ('Jack', 10),
             ('Queen', 10), ('King', 10)]
    suits = ['Spades', 'Diamonds', 'Hearts', 'Clubs']

    def __init__(self):
        """
        Initializes the deck by creating list of cards, iterating through all ranks and suits.
        """
        self._cards = []
        for r in self.ranks:
            for s in self.suits:
                self._cards.append(Card(r[1], r[0], s))

    def draw(self) -> Card:
        """
        Draws a card randomly from the deck without replacement.
        Returns: A tuple containing the card identifier and card value.
        """
        card = random.choice(self._cards)
        self._cards.remove(card)
        return card
