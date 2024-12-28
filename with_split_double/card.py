"""
Represents a Card in a blackjack game.

Attributes:
  value (int): Value of a card in a blackjack game.
  rank (str): Type of Card. 
  suit (str): Suit of Card.
"""


class Card():
    """
    Implement a basic playing card
    """

    def __init__(self, value=1, rank="Ace", suit="Spades"):
        """
        Initializes a new card given a value, rank, and suit.
        """
        self.value = value
        self.rank = rank
        self.suit = suit

    def __str__(self):
        """
        Prints how you would call a given card.
        """
        return self.rank + " of " + self.suit

    def get_rank(self):
        return self.rank

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
