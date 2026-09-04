import pandas as pd

df = pd.read_csv("./data/data.csv")

losers_per_date = df.groupby("Date")["Win"].apply(
    lambda x: (x == "No").sum()
)

# Dates with exactly one loser
single_loser_dates = losers_per_date[losers_per_date == 1].index

# Flag the person if they were the only loser that day
df["only_loser"] = (
    (df["Date"].isin(single_loser_dates)) &
    (df["Win"] == "No")
).astype(int)

rank_summary_df = df.groupby("Person").agg(
    win_percentage=("Win", lambda x: (x == "Yes").mean()*100),
    average_odds=("Odds", "mean"),
    rounds_played=("Person", "count"),
    weighted_wins = ("Odds", lambda x: x[df.loc[x.index, "Win"] == "Yes"].sum()),
    only_loser = ("only_loser", "sum")
).reset_index()

rank_summary_df['exp win perc'] = (1/rank_summary_df['average_odds'])*100
rank_summary_df['weighted_wins_avg'] = rank_summary_df['weighted_wins']/rank_summary_df['rounds_played'] 


overall_summary = df.groupby("Date").agg(
    win_count=('Win', lambda x: (x=="Yes").sum()/((x=="No").sum()+ (x=="Yes").sum())),
    weekly_odds=("Odds", "prod")
    ).reset_index()

wins = len(overall_summary[overall_summary['win_count']==1])

win_perc = wins/len(overall_summary) * 100

net_gain = (overall_summary[overall_summary['win_count']==1]['weekly_odds']*15).sum()-15*len(overall_summary)
