from constants import Constants
from player import Player
from card import Card
import numpy as np
import pandas as pd
"""
A reinforcement learning agent based on Q-learning. It extends the Player class 
and learns how to play the game of Blackjack optimally by updating its Q-values 
after a set number of rounds. Uses the epsilon-greedy strategy.

Attributes:
    _Q (dict): Q-value table that maps states (dealer hand value, player hand value) to action (hit/stay).
    _last_state (tuple): Stores state of game from last action taken by learner.
    _last_action (str): Stores last action take by learner (hit/stay).
    _learning_rate (float): Learning rate of Q-Learning algorithm. Defaults to 0.7.
    _discount (float): The discount factor of algorithm to control significance of rewards. Defaults to 0.9.
    _epsilon (float): The epsilon value for epsilon-greedy strategy to control exploration rate. Defaults to 0.9.
    _learning (bool): Indicates if learner is in learning phase.
    _split (bool): Indicates if the learner can split
    _can_double (bool): Indicates if the learner can double
    _has_doubled (bool): Indicates if the learner chose to double
    _action_list (list): Represents list of valid actions
"""


class QLearner(Player):
    _Q = {}  # Q-value table, state -> action-value pairs

    def __init__(self, last_state=None, last_action=None, learning_rate=0.001, discount_factor=0.8, epsilon=0.995):
        """
        Initializes Q-Learner with given parameters.
        """
        super().__init__()
        self._last_state = last_state
        self._last_action = last_action
        self._learning_rate = learning_rate
        self._discount = discount_factor
        self._epsilon = epsilon
        self._learning = True  # Set this to False after learning rounds
        self._split = False
        self._can_double = True
        self._has_doubled = False
        self._action_list = [Constants.hit, Constants.stay, Constants.double]

    def can_split(self):
        """
        Returns true if a player's current hand can split. 
        This is the case when the first two cards that are dealt to the 
        player have the same value.
        """
        return self._hand[0].rank == self._hand[1].rank

    def enable_split(self):
        """Enables the split option"""
        self._split = True

    def disable_split(self):
        """Disables the split option"""
        self._split = False

    def set_initial_split_hand(self, card: Card):
        """Initializes a new hand after splitting with one card"""
        self._hand = [card]
        # split aces are always 11
        self._total_hand_val = 11 if card.rank == "Ace" else card.value
        self._ace_count = 1 if card.rank == "Ace" else 0

    def get_action(self, state):
        """Choose an action using epsilon-greedy strategy"""
        # if the two cards are the same, set split flag to true in game.py
        if self._split == True and Constants.split not in self._action_list:
            self._action_list.append(Constants.split)

        if self._can_double == True and Constants.double not in self._action_list:
            self._action_list.append(Constants.double)
        # should be set to false in game.py if it's no longer the first move
        if self._can_double == False and Constants.double in self._action_list:
            self._action_list.remove(Constants.double)

        if state in QLearner._Q and np.random.uniform(0, 1) < self._epsilon:
            # all actions have same reward value
            if len(set(QLearner._Q[state].values())) == 1:
                action = np.random.choice(self._action_list)
            else:
                pos_actions = QLearner._Q[state].copy()

                # remove split if not possible action
                if not self._split and Constants.split in pos_actions:
                    del pos_actions[Constants.split]

                # remove double if not possible action
                if self._can_double == False and Constants.double in pos_actions:
                    del pos_actions[Constants.double]

                # Choose the action with the highest Q-value
                action = max(pos_actions, key=pos_actions.get)

        else:
            # Choose a random action (exploration)
            action = np.random.choice(self._action_list)
            # Initialize state-action pair if not already present
            if state not in QLearner._Q:
                QLearner._Q[state] = {
                    Constants.hit: 0, Constants.stay: 0, Constants.split: 0, Constants.double: 0}

        # Store last action and state for Q-value update
        self._last_state = state
        self._last_action = action

        # not sure if needed
        if self._split == True:
            self._action_list.remove(Constants.split)
            self._split = False

        return action

    def get_reward(self, state):
        """Return the reward of the state"""
        # Check if new_state exists in the Q-table
        if state in QLearner._Q:
            # Calculate the reward (discounted max Q-value for the next state)
            reward = max(QLearner._Q[state].values())
        else:
            reward = 0
        return reward

    def update(self, new_state, reward):
        """Update the Q-value based on the received reward"""
        try:
            if self._learning:
                old_value = QLearner._Q[self._last_state][self._last_action]
                future_reward = self._discount * self.get_reward(new_state)

                # Q-learning formula to update the Q-value
                QLearner._Q[self._last_state][self._last_action] = (1 - self._learning_rate) * old_value + \
                    self._learning_rate * (reward + future_reward)
        except KeyError as e:
            print(self._last_state, self._last_action)

    def split_update(self, state, reward):
        "Update the Q-value based on the received reward if the action was split"
        if self._learning:
            # print(QLearner._Q[state])
            old_value = QLearner._Q[state][Constants.split]
            future_reward = self._discount * reward

            # Q-learning formula to update the Q-value
            QLearner._Q[state][Constants.split] = (1 - self._learning_rate) * old_value + \
                self._learning_rate * future_reward

    def double_update(self, state, reward):
        "Update the Q-value based on the received reward if the action was double"
        if self._learning:
            old_value = QLearner._Q[state][Constants.double]
            future_reward = self._discount * (reward*2)

            # Q-learning formula to update the Q-value
            QLearner._Q[state][Constants.double] = (1 - self._learning_rate) * old_value + \
                self._learning_rate * future_reward

    def get_optimal_strategy(self):
        """Returns a DataFrame of optimal strategies based on Q-values"""
        df = pd.DataFrame(QLearner._Q).transpose()
        df.reset_index(inplace=True)

        card_order = {
            'Twos': 22, 'Threes': 23, 'Fours': 24, 'Fives': 25, 'Sixes': 26,
            'Sevens': 27, 'Eights': 28, 'Nines': 29, 'Tens': 30, 'Aces': 31
        }
        df.columns = ['player', 'dealer', 'hit', 'stay', 'split', 'double']

        def sort_key(value):
            if str(value).isdigit():
                return int(value)
            return card_order.get(value, 0)
        # Sort by 'player' and 'dealer' for organized output
        df['player_sort'] = df['player'].apply(sort_key)
        df = df.sort_values(by=['player_sort', 'dealer']).drop(
            columns='player_sort').reset_index(drop=True)

        def is_soft(value):
            return "," in value and value.split(",")[0] == "A" and value.split(",")[1].isdigit()
        for row, col in df.iterrows():
            if str(col['player']).isdigit() or is_soft(str(col['player'])):
                df.at[row, 'optimal'] = col[['hit', 'stay', 'double']].idxmax()
            else:
                df.at[row, 'optimal'] = col[[
                    'hit', 'stay', 'split', 'double']].idxmax()
        return df
