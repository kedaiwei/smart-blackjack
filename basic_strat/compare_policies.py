import pandas as pd

df_learner = pd.read_csv("optimal_policy.csv")
# Select 1nd, 2rd, and 5th columns
df_learner = df_learner.iloc[:, [0, 1, 4]]
print(df_learner)

df_basic = pd.read_csv("basic_strat.csv")
print(df_basic)

diff = pd.concat([df_basic, df_learner]).drop_duplicates(keep=False)
print(diff)

diff.to_csv("diff.csv", index=False)
