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
    weekly_odds=("Odds", "prod"),
    players=("Person", "count")
    ).reset_index()

overall_summary['potential prize money (£)'] = round(overall_summary['weekly_odds']*(overall_summary['players']*3), 2)
overall_summary["Winning per person"] = overall_summary["potential prize money (£)"]/overall_summary['players']

wins = len(overall_summary[overall_summary['win_count']==1])

win_perc = wins/len(overall_summary) * 100

in_pot = (overall_summary[overall_summary['win_count']==1]['potential prize money (£)']).sum()

net_gain = in_pot - len(df)*3
#net_gain = (overall_summary[overall_summary['win_count']==1]['weekly_odds']*15).sum()-15*len(overall_summary)

def winnings_per_person(person, win_dates):
    winnings_total = 0
    for date in win_dates:
        if person in list(df[df['Date'] == (date)]['Person']):
            winnings_total += overall_summary[overall_summary.index == win_dates[0]]["Winning per person"]
    print(float(winnings_total))
    return float(winnings_total)

print(overall_summary)
win_dates = list(overall_summary[overall_summary['win_count']==1].index)

spin_winnings = winnings_per_person("Spin", win_dates=win_dates)
rambo_winnings = winnings_per_person("Rambo", win_dates=win_dates)
beth_winnings = winnings_per_person("Beth", win_dates=win_dates)
grizz_winnings = winnings_per_person("Grizz", win_dates=win_dates)
zed_winnings = winnings_per_person("Zed", win_dates=win_dates)