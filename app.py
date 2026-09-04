import streamlit as st
import pandas as pd
import plotly.express as px

from data_cleaning import rank_summary_df, overall_summary, wins, win_perc, net_gain, df

st.set_page_config(
    page_title="Family Coupon",
    layout="wide"
)

# ----------------------------

# Header

# ----------------------------

st.title("⚽ Simpson Coupon Builder Dashboard")



# ----------------------------

# KPI Cards

# ----------------------------

c1, c2, c3, c4 = st.columns(4)



c1.metric("Weeks Played", len(overall_summary))

c2.metric("Perfect Weeks %", f"{win_perc:.1f}%")

c3.metric("Net Gain (£)", f"{net_gain:.2f}")

c4.metric(

"Weighted Wins AVG",

rank_summary_df.sort_values(

"weighted_wins_avg",

ascending=False

).iloc[0]["Person"]

)



# ----------------------------

# Tabs

# ----------------------------

tab1, tab2, tab3 = st.tabs(

["🏆 Player Rankings", "📈 Weekly Results", "📋 Raw Data"]

)



# ============================

# Player Rankings

# ============================

with tab1:



    st.subheader("Player Rankings")


    ranking_view = rank_summary_df.sort_values(
        "weighted_wins_avg",
        ascending=False
    ).reset_index(drop=True)

    ranking_view.insert(0, "Rank", range(1, len(ranking_view)+1))

    st.dataframe(
        ranking_view.style.hide(axis="index").format({
            "win_percentage": "{:.1f}",
            "average_odds": "{:.2f}",
            "exp_win_perc": "{:.1f}",
            "weighted_wins": "{:.2f}", 
            "weighted_wins_avg": "{:.2f}",
            "exp win perc": "{:.2f}",
        }),
        hide_index = True,
        use_container_width=True
    )



    fig = px.bar(
        ranking_view,
        x="Person",
        y="win_percentage",
        color="Person",
        title="Win Percentage"

    )



    st.plotly_chart(fig, use_container_width=True)



# ============================

# Weekly Results

# ============================

with tab2:

    st.subheader("Weekly Results")

    overall_summary["Date"] = pd.to_datetime(
        overall_summary["Date"],
        dayfirst=True
    ).dt.date

    overall_summary_adj = overall_summary.copy()

    overall_summary_adj['Win Percentage'] = (overall_summary_adj['win_count'] * 100).astype(str) +"%"

    st.dataframe(
        overall_summary_adj.drop(columns=["win_count"]).style.format({
            "weekly_odds": "{:.1f}",
        }),
        hide_index = True,
        use_container_width=True
    )




    fig = px.line(
        overall_summary,
        x="Date",
        y="win_count",
        markers=True,
        title="Weekly Hit Rate"
    )



    #st.plotly_chart(fig, use_container_width=True)



    #fig2 = px.bar(
    #    overall_summary,
    #    x="Date",
    #    y="weekly_odds",
    #    title="Combined Weekly Odds"
    #)



    #st.plotly_chart(fig2, use_container_width=True)

# ============================
# Raw Data
# ============================

with tab3:



    person = st.selectbox(
        "Filter by Person",
        ["All"] + sorted(df["Person"].unique())
    )

    display_df = df.copy()

    if person != "All":
        display_df = display_df[
            display_df["Person"] == person
    ]
        
    st.dataframe(display_df, use_container_width=True)