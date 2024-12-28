import random
"""
Represents a standard deck of playing cards in blackjack. Has attributes and 
methods that allows for storing values of cards as well as drawing cards at random 
without replacement. 

Attributes:
  _card_def (dict): A dictionary that maps card identifiers to respective values.
  _cards (list): A list containing all playing cards in blackjack. 
"""


class Deck:
    def __init__(self):
        """
        Initializes the deck by defining card values and creating list of cards.
        """
        self._card_def = {
            '2H': 2, '3H': 3, '4H': 4, '5H': 5, '6H': 6, '7H': 7, '8H': 8, '9H': 9,
            '10H': 10, 'JH': 10, 'QH': 10, 'KH': 10, 'AH': 11,

            '2D': 2, '3D': 3, '4D': 4, '5D': 5, '6D': 6, '7D': 7, '8D': 8, '9D': 9,
            '10D': 10, 'JD': 10, 'QD': 10, 'KD': 10, 'AD': 11,

            '2C': 2, '3C': 3, '4C': 4, '5C': 5, '6C': 6, '7C': 7, '8C': 8, '9C': 9,
            '10C': 10, 'JC': 10, 'QC': 10, 'KC': 10, 'AC': 11,

            '2S': 2, '3S': 3, '4S': 4, '5S': 5, '6S': 6, '7S': 7, '8S': 8, '9S': 9,
            '10S': 10, 'JS': 10, 'QS': 10, 'KS': 10, 'AS': 11
        }

        self._cards = ['AH', 'AD', 'AC', 'AS', '2H', '2D', '2C', '2S', '3H',
                       '3D', '3C', '3S', '4H', '4D', '4C', '4S', '5H', '5D',
                       '5C', '5S', '6H', '6D', '6C', '6S', '7H', '7D', '7C',
                       '7S', '8H', '8D', '8C', '8S', '9H', '9D', '9C', '9S',
                       '10H', '10D', '10C', '10S', 'JH', 'JD', 'JC', 'JS', 'QH',
                       'QD', 'QC', 'QS', 'KH', 'KD', 'KC', 'KS']

    def draw(self):
        """
        Draws a card randomly from the deck without replacement.
        Returns: A tuple containing the card identifier and card value.
        """
        card = random.sample(self._cards, 1)[0]
        return (card, self._card_def[card])
