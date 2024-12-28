from constants import Constants
from dealer import Dealer
from deck import Deck
from q_learner import QLearner
import matplotlib.pyplot as plt

"""
Designed to simulate and run the game of Blackjack using a Q-Learner agent.
By playing a certain number of rounds, the learner makes optimal decisions 
to increase the win probability. The class also tracks the win rate and
reward (profit/loss) over time and contains tools to plot the win rate over time.

Attributes:
    learner (Learner): The Q-Learner agent that learns and plays game. Defaults to QLearner if not provided.
    num_learning_rounds (int): The total number of rounds to be played for learning.
    report_every (int): The frequency at which the current win rate is reported. Default to 100.
    win (int): Counts the number of games learner has won.
    loss (int): Counts the number of games learner has lost.
    tie (int): Counts the number of games learner has tied.
    game_count (int): The total number of rounds played (learning and testing).
    win_rate_history (list): A list storing the win rate after each game.
    reward_history (list): A list storing cumulative rewards after each game.
    reward (int): Tracks the cumulative reward. 
"""


class Game:
    def __init__(self, num_learning_rounds, learner=None, report_every=100):
        """
        Initializes a new game instance with initial settings.
        """
        # Default to QLearner if not provided
        self.learner = learner if learner else QLearner()
        self.num_learning_rounds = num_learning_rounds
        self.report_every = report_every
        self.win = 0
        self.loss = 0
        self.tie = 0
        self.game_count = 1
        self.win_rate_history = []  # List to store win rates over time
        self.reward_history = []
        self.reward = 0

    def run(self):
        """
        Runs the blackjack game for a set number of learning rounds.
        In each round, the function resets the game state, player and dealer 
        take turns acting based on corresponding policies, and the learner updates
        its Q-values based on the outcome of the game. Win rates and rewards are
        tracked after each round.
        """
        for _ in range(self.num_learning_rounds):
            deck, player, dealer, winner = self.reset_round()
            state = self.get_state(player, dealer)

            # Test for blackjack first
            blackjack = False
            if player.get_hand_value() == 21:
                blackjack = True
                if dealer.get_hand_value() != 21:
                    winner = Constants.player1

            while not winner and not blackjack:
                # Run player actions
                player_action = player.get_action(state)
                if player_action == Constants.hit:
                    player.hit(deck)
                else:  # action is to stay
                    break

                if self.is_bust(player):
                    winner = Constants.player2
                    break

                # Update state and continue
                state = self.get_state(player, dealer)
                player.update(state, 0)

            while not winner and not blackjack:
                dealer_action = dealer.get_action()
                if dealer_action == Constants.hit:
                    dealer.hit(deck)
                else:  # action is to stay
                    break
                if self.is_bust(dealer):
                    winner = Constants.player1
                    break

            # Finalize the game and update Q-values with the result
            if winner is None:
                winner = self.determine_winner(player, dealer)
            reward = 0
            if winner == Constants.player1:
                self.win += 1
                reward = 1.5 if blackjack else 1
                player.update(self.get_final_state(
                    player, dealer), reward)  # Win 3:2 reward

            elif winner == Constants.player2:
                self.loss += 1
                player.update(self.get_final_state(
                    player, dealer), -1)  # Loss penalty
                reward = -1

            else:
                self.tie += 1
                player.update(self.get_final_state(
                    player, dealer), 0)
                reward = 0

            self.reward += reward
            self.reward_history.append(self.reward)

            self.game_count += 1
            self.update_win_rate()
            self.report()

        # End of learning
        print("Learning finished!")
        self.learner._learning = False

    def update_win_rate(self):
        """
        Calculates the current win rate and stores it in the win_rate_history list.
        """
        total_games = self.win + self.loss
        if total_games > 0:
            win_rate = self.win / total_games
            self.win_rate_history.append(win_rate)

    def report(self):
        """
        Reports the current win rate at intervals of self.report_every.
        """
        if self.game_count % self.num_learning_rounds == 0:
            win_rate = self.win / (self.win + self.loss)
            print(f"Game {self.game_count}: Win rate = {win_rate}")
        elif self.game_count % self.report_every == 0:
            win_rate = self.win / (self.win + self.loss)
            print(f"Game {self.game_count}: Current win rate = {win_rate}")

    def get_state(self, player: QLearner, dealer: Dealer):
        """
        Return a tuple representing the state: player's hand value and dealer's showing value
        """
        return (player.get_hand_value(), dealer.get_original_showing_value())

    def get_final_state(self, player: QLearner, dealer: Dealer):
        """Final state is the hand values of both players"""
        return (player.get_hand_value(), dealer.get_hand_value())

    def determine_winner(self, player: QLearner, dealer: Dealer):
        """Determine the winner based on hand values"""
        player_value = player.get_hand_value()
        dealer_value = dealer.get_hand_value()

        if player_value > dealer_value:
            return Constants.player1
        elif player_value < dealer_value:
            return Constants.player2
        else:
            return None

    def is_bust(self, player: QLearner):
        """Check if a player has gone bust (hand value > 21)"""
        return player.get_hand_value() > 21

    def reset_round(self):
        """Reset the game state and deal cards to players"""
        deck = Deck()
        player = self.learner
        dealer = Dealer()

        player.reset_hand()
        dealer.reset_hand()

        # Initial card deal
        player.hit(deck)
        dealer.hit(deck)
        player.hit(deck)
        dealer.hit(deck)

        return deck, player, dealer, None

    def plot_win_rate(self):
        """Plot the win rate history"""
        plt.figure(figsize=(10, 6))
        plt.plot(self.win_rate_history, label="Win Rate")
        plt.xlabel("Games Played")
        plt.ylabel("Win Rate")
        plt.title("Win Rate Over Time")
        plt.legend()
        plt.show()

    def plot_profit_loss(self):
        """Plot the reward history"""
        plt.figure(figsize=(10, 6))
        plt.plot(self.reward_history, label="Profit/Loss")
        plt.xlabel("Games Played")
        plt.ylabel("Profit/Loss")
        plt.title("Profit/Loss Over Time")
        plt.legend()
        plt.show()
