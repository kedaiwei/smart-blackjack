# JL_Smart-Blackjack_el592_emk255_kw462_mbj49
Max: Player and Dealer classes govern the two agents who play a game of blackjack. The Dealer class is governed by strict rules as is a dealer on a blackjack table. They must hit until they get at least 17. The player has a more complex structure in order to expand to handle different actions decided later by the learning agent. The final part I worked on was the Deck class. It needed to be changed drastically from the structure it had in the aid code. We want to be able to track the cards taken later in order to count cards and beat the house. In its current state the data structure is a dictionary that maps card names to their in game values. The draw function now takes a random sample with replacement but later will take without replacement to instill the memory factor of blackjack into our project. \
Elliot: Originally, the aid code just had a Player class where a Q-Learner was a subclass of player. However, we realized that the dealer and player have different standards in taking action, so I created a separate Dealer class where it is also a subclass of Player. The aid code also had incorrect game implementation and my role was to identify these errors and fix them. First, the aid code defaulted the dealer to stay from 15 and above, but the correct value should have been 17. Second, the gameplay was coded such that the player and dealer alternate taking actions, but this was incorrect in that the players must take all the actions first, while the dealer taking action once the player stays and has not busted. Finally, the game did not take into account Aces, since an Ace plays as a 1 or 11, depending on the other cards in a player’s hand. So I was able to add a separate attribute in the Player class and modified the get_hand_value function to incorporate such values. \
Katie: The AI agent we decided to use was Q-Learning because it’s a model-free reinforcement learning algorithm that works well in environments with discrete states and actions, like blackjack. The state of our environment consists of the sum of the player’s current cards and the dealer’s visible card. We utilize an epsilon greedy strategy where 90% of the time, the agent is exploiting (determining the best policy from previous rollouts) and 10% of the time the agent uses a random number generator to determine which actions to take. As of right now, the only actions are to hit or to stay. The transition function chooses the action with the highest reward. Rewards are determined by the game state which is a +1.5 for blackjack, +1 for winning, 0 for ties, and -1 for losing. The state is updated each time the player hits and once more after the dealer hits. \ 
Eric: After training for 100000 games, we get our optimal policy where hit and stay columns represent the q-value or expected reward. Our policy has some deviations from blackjack basic strategy, but we see that we come to a win rate near 42%. This is on par with the win rate of the basic strategy of blackjack which has a win rate of around 42.22%. And we haven’t yet implemented the option to split or double which should boost our profit/loss by a large margin. \

To run the training: \ 

python with_split_double/main.py


Requirements/installations: \
iniconfig==2.0.0
numpy==2.1.3
packaging==24.2
pandas==2.2.3
pluggy==1.5.0
pytest==8.3.3
python-dateutil==2.9.0.post0
pytz==2024.2
six==1.16.0
tzdata==2024.2
