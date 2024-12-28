import pytest
from q_learner import QLearner
from card import Card
from deck import Deck
from constants import Constants

def test_initial_state():
    qlearner = QLearner()
    assert qlearner._learning_rate == 0.005
    assert qlearner._discount == 0.9
    assert qlearner._epsilon == 0.95
    assert qlearner._learning is True
    assert qlearner._action_list == [Constants.hit, Constants.stay, Constants.double]

def test_can_split():
    qlearner = QLearner()
    qlearner._hand = [Card(10, "10", "Spades"), Card(10, "10", "Hearts")]
    assert qlearner.can_split()

def test_cannot_split_different_values():
    qlearner = QLearner()
    qlearner._hand = [Card(10, "10", "Spades"), Card(9, "9", "Hearts")]
    assert not qlearner.can_split()

def test_set_initial_split_hand():
    qlearner = QLearner()
    qlearner.set_initial_split_hand(Card(10, "10", "Spades"))
    assert len(qlearner.get_hand()) == 1
    assert qlearner._total_hand_val == 10
    assert qlearner._ace_count == 0

def test_set_initial_split_hand_with_ace():
    qlearner = QLearner()
    qlearner.set_initial_split_hand(Card(1, "Ace", "Spades"))
    assert len(qlearner.get_hand()) == 1
    assert qlearner._total_hand_val == 11
    assert qlearner._ace_count == 1

def test_get_action_epsilon_greedy():
    qlearner = QLearner()
    state = (15, 10)  # Mock state
    qlearner._Q = {
        state: {Constants.hit: 0.5, Constants.stay: 0.8, Constants.split: 0.2, Constants.double: 0.1}
    }
    qlearner._epsilon = 1.0  # Force greedy selection
    action = qlearner.get_action(state)
    assert action == Constants.stay

def test_get_action_exploration():
    qlearner = QLearner()
    state = (15, 10)  # Mock state
    qlearner._Q = {}
    qlearner._epsilon = 0.0  # Force exploration
    action = qlearner.get_action(state)
    assert action in qlearner._action_list

def test_update_q_value():
    qlearner = QLearner()
    state = (15, 10)
    qlearner._Q[state] = {Constants.hit: 0.5, Constants.stay: 0.8}
    qlearner._last_state = state
    qlearner._last_action = Constants.hit

    qlearner.update(new_state=(16, 10), reward=1.0)
    assert qlearner._Q[state][Constants.hit] != 0.5

def test_split_update():
    qlearner = QLearner()
    state = (15, 10)
    qlearner._Q[state] = {Constants.split: 0.5}
    qlearner.split_update(state, reward=1.0)
    assert qlearner._Q[state][Constants.split] > 0.5

def test_double_update():
    qlearner = QLearner()
    state = (15, 10)
    qlearner._Q[state] = {Constants.double: 0.5}
    qlearner.double_update(state, reward=1.0)
    assert qlearner._Q[state][Constants.double] > 0.5
