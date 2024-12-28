"""
Represents a player in the Blackjack table, including the dealer.

Attributes:
    _hand(list): A list that stores cards dealt to player
    _total_hand_val (int): The total value of player's hand incoporating Aces.
    _ace_count (int): Tracks the number of Aces in player's hand
"""
from deck import Deck
from card import Card
from typing import List


class Player:
    def __init__(self):
        """
        Initializes a new Player with empty hand with 0 total value and 0 aces.
        """
        self._hand: List[Card] = []
        self._total_hand_val = 0
        self._ace_count = 0

    def __str__(self):
        hand_str = ', '.join(str(card) for card in self._hand)
        return f"Hand: {hand_str} | Total Value: {self._total_hand_val}"

    def get_hand(self):
        """
        Returns: The list of a player's current hand.
        """
        return tuple(self._hand)

    def get_hand_value(self):
        """
        Returns: The total value of a player's current hand.
        """
        if self._ace_count > 0 and self._total_hand_val > 21:
            self._total_hand_val -= 10
            self._ace_count -= 1
        return self._total_hand_val

    def hit(self, deck: Deck):
        """
        Draws a single card from the deck, adjust the updated Ace count, 
        total value, and new hand accordingly.
        """
        card = deck.draw()
        if card.get_rank() == "Ace":
            self._ace_count += 1
            if self._total_hand_val > 10:
                card.set_value(1)
            else:
                card.set_value(11)
        self._total_hand_val += card.get_value()
        self._hand.append(card)

    def reset_hand(self):
        """
        Resets a player's hand to its intial state.
        """
        self._hand = []
        self._total_hand_val = 0
        self._ace_count = 0
        self._has_doubled = False
        self._can_double = True

    def show_hand(self):
        hand = []
        for card in self._hand:
            hand.append(card.get_rank())
        return hand
