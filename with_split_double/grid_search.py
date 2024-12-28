import pandas as pd
from game import Game
from q_learner import QLearner
import itertools


def main():
    """
    Tests for the optimal parameters for Q-Learner using grid search method.
    """
    learning_rates = [0.001, 0.005, 0.01, 0.1, 0.2, 0.5, 1.0]
    discount_factors = [0.8, 0.9, 0.95, 0.99]
    epislon_values = [0.9, 0.95, 0.99, 0.995, 0.999]
    num_learning_rounds = 20000
    best_params = None
    best_val = -float('inf')
    best_win_rate = -float('inf')

    rows = []
    for learning_rate, discount_factor, epsilon in itertools.product(learning_rates, discount_factors, epislon_values):

        game = Game(
            num_learning_rounds,
            QLearner(
                learning_rate=learning_rate,
                discount_factor=discount_factor,
                epsilon=epsilon
            )
        )
        number_of_test_rounds = 50
        for _ in range(0, number_of_test_rounds):
            game.run()
        final_profit = game.get_reward()
        win_rate = game.win / (game.win + game.loss + game.tie)
        if final_profit > best_val:
            best_params = (learning_rate, discount_factor, epsilon)
            best_val = final_profit
            best_win_rate = win_rate
        rows.append({"learning_rate":learning_rate, "discount_factor":discount_factor, "epsilon":epsilon, "win_rate":win_rate, "profit":final_profit})
        print(
            f"Learning Rate: {learning_rate}, Discount Factor: {discount_factor}, Epsilon: {epsilon}, Win Rate: {win_rate}, Profit: {final_profit}")
    df = pd.DataFrame(rows)
    df.to_csv("grid_search.csv", index=False)
    print(
        f"Best Parameters: Learning Rate: {best_params[0]}, Discount Factor: {best_params[1]}, Epsilon: {best_params[2]}")
    print(f"Best Win Rate: {best_win_rate}")


if __name__ == "__main__":
    main()
