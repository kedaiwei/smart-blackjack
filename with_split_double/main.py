from game import Game
from q_learner import QLearner


def main():
    """
    Sets up game environment, executes series of learning rounds, then plots the 
    results of agent's performance over time. Also outputs the optimal strategy 
    learned by the Q-learner to a csv file. 
    """
    num_learning_rounds = 200000
    game = Game(num_learning_rounds, QLearner())  # Q learner
    number_of_test_rounds = 500
    for _ in range(0, number_of_test_rounds):
        game.run()

    # plot win rate for each round
    game.plot_win_rate()
    game.plot_profit_loss()

    df = game.learner.get_optimal_strategy()
    print(df)
    df.to_csv('optimal_policy.csv', index=False)
    print(f"profit/loss: {(game.reward)}")


if __name__ == "__main__":
    main()
