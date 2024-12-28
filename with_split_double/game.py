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


def perform_hit(hand: QLearner, deck: Deck):
    hand.hit(deck)
    hand._can_double = False


def perform_stay(hand: QLearner, staying_hands: list):
    staying_hands.append(hand)
    hand._can_double = False


def perform_split(hand: QLearner, staying_hands: list, hands: list, deck: Deck,
                  get_state, orig_hand, dealer: Dealer):
    is_pair = (orig_hand[0].get_value() == orig_hand[1].get_value())
    assert is_pair or pair_of_aces(orig_hand)
    assert len(orig_hand) == 2

    p1 = QLearner(hand._last_state, hand._last_action)
    p2 = QLearner(hand._last_state, hand._last_action)
    p1.set_initial_split_hand(hand.get_hand()[0])
    p1.hit(deck)
    state = get_state(p1, dealer)
    p1.update(state, 0)

    p2.set_initial_split_hand(hand.get_hand()[1])
    p2.hit(deck)
    state = get_state(p2, dealer)
    p2.update(state, 0)
    if pair_of_aces(orig_hand):
        staying_hands.extend([p1, p2])
    else:
        hands.extend([p1, p2])


# needs updating so that hand is kept as doubled and reward is doubled
def perform_double(hand: QLearner, deck: Deck):
    hand.hit(deck)
    hand._can_double = False
    hand._has_doubled = True


def pair_of_aces(hand):
    return hand[0].rank == "Ace" and hand[1].rank == "Ace"


class Game:
    SPECIAL_DECK = {(2, 2): "2,2", (3, 3): "3,3", (4, 4): "4,4", (5, 5): "5,5",
                    (6, 6): "6,6", (7, 7): "7,7", (8, 8): "8,8", (9, 9): "9,9",
                    (10, 10): "10,10", (11, 1): "A,A"}  # (1,11) not possible with ace impl

    for i in range(2, 10):  # Add Aces table
        SPECIAL_DECK[(i, 11)] = f"A,{i}"
        SPECIAL_DECK[(11, i)] = f"A,{i}"

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

    def get_reward(self):
        return self.reward

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
            orig_player = player
            orig_hand = player.get_hand()

            # handle blackjack
            if player.get_hand_value() == 21 and dealer.get_hand_value() != 21:
                self.win += 1
                self.reward += 1.5
                player.update(self.get_final_state(
                    player, dealer), 1.5)
                continue
            elif player.get_hand_value() == 21 and dealer.get_hand_value() == 21:
                self.tie += 1
                player.update(self.get_final_state(
                    player, dealer), 0)
                continue
            elif player.get_hand_value() != 21 and dealer.get_hand_value() == 21:
                self.loss += 1
                self.reward -= 1
                player.update(self.get_final_state(
                    player, dealer), -1)
                continue

            staying_hands = []
            hands = [player]
            split = False
            cum_reward = 0
            idx = 0
            while idx < len(hands):
                hand = hands[idx]
                state = self.get_state(hand, dealer)
                while True:
                    hand.disable_split()
                    if hand.can_split():
                        hand.enable_split()

                    action = player.get_action(state)

                    if action == Constants.hit:  # hits
                        perform_hit(hand, deck)
                        if self.is_bust(hand):
                            cum_reward -= 1
                            self.loss += 1
                            break

                    elif action == Constants.stay:  # stays
                        perform_stay(hand, staying_hands)
                        break

                    elif action == Constants.split:  # splits
                        split = True
                        self.game_count += 1

                        perform_split(hand, staying_hands, hands,
                                      deck, self.get_state, orig_hand, dealer)
                        break

                    elif action == Constants.double:
                        perform_double(hand, deck)
                        if self.is_bust(hand):
                            cum_reward -= 2
                            self.loss += 1
                            break

                        staying_hands.append(hand)  # must stay after doubled
                    state = self.get_state(hand, dealer)
                    player.update(state, 0)

                idx += 1
            dealer_bust = False

            if len(staying_hands) != 0:  # if there is a staying hand
                # dealer's turn
                while dealer.get_hand_value() <= 17:
                    if dealer.get_hand_value() == 17 and dealer._ace_count > 0:
                        dealer.hit(deck)
                    else:
                        dealer.hit(deck)
                        if self.is_bust(dealer):
                            dealer_bust = True
                            break
            # Play staying hands against same dealer
            for hand in staying_hands:
                winner = self.determine_winner(hand, dealer)
                if dealer_bust or winner == Constants.player1:
                    if hand._has_doubled:
                        cum_reward += 2
                    else:
                        cum_reward += 1
                    self.win += 1

                elif winner == Constants.player2:
                    self.loss += 1
                    if hand._has_doubled:
                        cum_reward -= 2
                    else:
                        cum_reward -= 1
                else:
                    self.tie += 1
            if split:
                # Update original hand with cumulative reward
                orig_player.split_update(self.get_state(
                    orig_player, dealer), cum_reward)
            orig_player.update(self.get_final_state(
                orig_player, dealer), cum_reward)
            self.reward += cum_reward
            self.reward_history.append(self.reward)
            self.game_count += 1
            self.update_win_rate()
            self.report()

        # End of learning
        # print("Learning finished!")
        self.learner._learning = False

    def update_win_rate(self):
        """
        Calculates the current win rate and stores it in the win_rate_history list.
        """
        total_games = self.win + self.loss + self.tie
        if total_games > 0:
            win_rate = self.win / total_games
            self.win_rate_history.append(win_rate)

    def report(self):
        """
        Reports the current win rate at intervals of self.report_every.
        """
        if self.game_count % self.num_learning_rounds == 0:
            win_rate = self.win / (self.win + self.loss + self.tie)
            print(f"Game {self.game_count}: Win rate = {win_rate}")
        elif self.game_count % self.report_every == 0:
            win_rate = self.win / (self.win + self.loss + self.tie)
            print(f"Game {self.game_count}: Current win rate = {win_rate}")

    def get_state(self, player: QLearner, dealer: Dealer):
        """
        Return a tuple representing the state: player's hand value and dealer's showing value
        """
        # update hand values from special deck when same value card is presented
        hand = (player.get_hand()[0].value, player.get_hand()[1].value)
        if hand in Game.SPECIAL_DECK:
            return (Game.SPECIAL_DECK[hand], dealer.get_original_showing_value())
        return (player.get_hand_value(), dealer.get_original_showing_value())

    def get_final_state(self, player: QLearner, dealer: Dealer):
        """Final state is the hand values of both players"""
        hand = (player.get_hand()[0].value, player.get_hand()[1].value)
        if hand in Game.SPECIAL_DECK:
            return (Game.SPECIAL_DECK[hand], dealer.get_hand_value())
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
