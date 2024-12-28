import pandas as pd

df_learner = pd.read_csv("optimal_policy.csv")
# Select 1nd, 2rd, and 5th columns
df_learner = df_learner.iloc[:, [0, 1, 6]]
print(df_learner)

df_basic = pd.read_csv("basic_strat.csv")
print(df_basic)

# diff = pd.concat([df_basic, df_learner]).drop_duplicates(keep=False)
merge_df = pd.merge(df_learner, df_basic, on=['player', 'dealer'], suffixes=('_learner', '_basic'))

# print(diff)
merge_df.to_csv('merged.csv', index=False)
# diff.to_csv("diff.csv", index=False)
