from constants import Constants
from player import Player
"""
Represents the dealer in the Blackjack game. Extends the Player class.

While inheritting most behaviors of Player class, the Dealer is different from 
other players on the table in that they must hit when their value is less than 17.
The Dealer also shows the first card initially.

"""


class Dealer(Player):
    def __init__(self):
        """
        Inherits Player's constructor.
        """
        super().__init__()

    def get_original_showing_value(self):
        """
        Returns: the value of dealer's first card that is visible to players.
        """
        return self._hand[0]

    def get_action(self):
        """
        Determine's dealer's action based on the total hand value. 
        If the total hand value is less than 17, the dealer must hit, else
        the dealer stays.
        """
        if self.get_hand_value() < 17:
            return Constants.hit
        else:
            return Constants.stay
