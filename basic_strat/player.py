"""
Represents a player in the Blackjack table, including the dealer.

Attributes:
    _hand(list): A list that stores cards dealt to player
    _total_hand_val (int): The total value of player's hand incoporating Aces.
    _ace_count (int): Tracks the number of Aces in player's hand
"""


class Player:
    def __init__(self):
        """
        Initializes a new Player with empty hand with 0 total value and 0 aces.
        """
        self._hand = []
        self._total_hand_val = 0
        self._ace_count = 0

    def get_hand(self):
        """
        Returns: The list of a player's current hand.
        """
        return self._hand

    def get_hand_value(self):
        """
        Returns: The total value of a player's current hand.
        """
        if self._ace_count > 0 and self._total_hand_val > 21:
            self._total_hand_val -= 10
            self._ace_count -= 1
        return self._total_hand_val

    def hit(self, deck):
        """
        Draws a single card from the deck, adjust the updated Ace count, 
        total value, and new hand accordingly.
        """
        card_name, card_value = deck.draw()
        if 'A' in card_name:  # implement ace
            self._ace_count += 1
        self._total_hand_val += card_value
        # ace implementation not accounted for here
        self._hand.append(card_value)

    def reset_hand(self):
        """
        Resets a player's hand to its intial state.
        """
        self._hand = []
        self._total_hand_val = 0
        self._ace_count = 0
