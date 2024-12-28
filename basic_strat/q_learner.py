from constants import Constants
from player import Player
import numpy as np
import pandas as pd
"""
A reinforcement learning agent based on Q-learning. It extends the Player class and learns how to play the game of Blackjack optimally by updating its Q-values after a set number of rounds. Uses the epsilon-greedy strategy.
Attributes:
    _Q (dict): Q-value table that maps states (dealer hand value, player hand value) to action (hit/stay).
    _last_state (tuple): Stores state of game from last action taken by learner.
    _last_action (str): Stores last action take by learner (hit/stay).
    _learning_rate (float): Learning rate of Q-Learning algorithm. Defaults to 0.7.
    _discount (float): The discount factor of algorithm to control significance of rewards. Defaults to 0.9.
    _epsilon (float): The epsilon value for epsilon-greedy strategy to control exploration rate. Defaults to 0.9.
    _learning (bool): Indicates if learner is in learning phase.
"""


class QLearner(Player):
    def __init__(self, learning_rate=0.7, discount_factor=0.9, epsilon=0.9):
        """
        Initializes Q-Learner with given parameters.
        """
        super().__init__()
        self._Q = {}  # Q-value table, state -> action-value pairs
        self._last_state = None
        self._last_action = None
        self._learning_rate = learning_rate
        self._discount = discount_factor
        self._epsilon = epsilon
        self._learning = True  # Set this to False after learning rounds

    def get_action(self, state):
        """Choose an action using epsilon-greedy strategy"""
        if state in self._Q and np.random.uniform(0, 1) < self._epsilon:

            # all actions have same reward value
            if len(set(self._Q[state].values())) == 1:
                action = np.random.choice([Constants.hit, Constants.stay])
            else:
                # Choose the action with the highest Q-value
                action = max(self._Q[state], key=self._Q[state].get)
        else:
            # Choose a random action (exploration)
            action = np.random.choice([Constants.hit, Constants.stay])
            # Initialize state-action pair if not already present
            if state not in self._Q:
                self._Q[state] = {Constants.hit: 0, Constants.stay: 0}

        # Store last action and state for Q-value update
        self._last_state = state
        self._last_action = action

        return action

    def update(self, new_state, reward):
        """Update the Q-value based on the received reward"""
        if self._learning:
            old_value = self._Q[self._last_state][self._last_action]
            # Check if new_state exists in the Q-table
            if new_state in self._Q:
                # Calculate the future reward (discounted max Q-value for the next state)
                future_reward = self._discount * \
                    max(self._Q[new_state].values())
            else:
                future_reward = 0

            # Q-learning formula to update the Q-value
            self._Q[self._last_state][self._last_action] = (1 - self._learning_rate) * old_value + \
                self._learning_rate * (reward + future_reward)

    def get_optimal_strategy(self):
        """Returns a DataFrame of optimal strategies based on Q-values"""
        df = pd.DataFrame(self._Q).transpose()
        df.reset_index(inplace=True)
        df.columns = ['player', 'dealer', 'hit', 'stay']
        df['optimal'] = df.apply(lambda x: Constants.hit if x[Constants.hit]
                                 > x[Constants.stay] else Constants.stay, axis=1)
        df = df.sort_values(by=['player', 'dealer'])

        return df
