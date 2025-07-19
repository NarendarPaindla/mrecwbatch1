import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

# 1. Page config — must be first Streamlit call
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. Data preparation
np.random.seed(42)
df = pd.DataFrame({
    "date": pd.date_range("2025-01-01", periods=90, freq="D"),
    "sales": np.random.randint(100, 500, size=90),
    "region": np.random.choice(["North", "South", "East", "West"], size=90)
})

# 3. Create two tabs
tab1, tab2 = st.tabs(["Time Series", "By Region"])

# --- TAB 1: Time Series ---
with tab1:
    st.header("Sales Over Time")
    # layout: two columns (charts side by side)
    col1, col2 = st.columns([2, 1], gap="medium")

    # Left: Daily sales line chart (Matplotlib)
    with col1:
        # Metric above chart
        total_sales = df["sales"].sum()
        st.metric("Total Sales (All Time)", f"{total_sales:,}")

        # Matplotlib figure
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(df["date"], df["sales"], marker="o", linewidth=1, label="Daily Sales")
        ax.set_xlabel("Date")
        ax.set_ylabel("Sales")
        ax.set_title("Daily Sales Over Time")
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend()
        st.pyplot(fig)

    # Right: 7‑day rolling average (Plotly)
    with col2:
        rolling = df.set_index("date")["sales"].rolling(window=7).mean().reset_index()
        last_avg = rolling["sales"].iloc[-1]
        st.metric("7‑Day Avg (Most Recent)", f"{last_avg:.2f}")

        fig2 = px.line(
            rolling,
            x="date",
            y="sales",
            title="7‑Day Rolling Average",
            labels={"sales": "7‑Day Avg", "date": "Date"},
        )
        fig2.update_layout(margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig2, use_container_width=True)

# --- TAB 2: By Region ---
with tab2:
    st.header("Sales by Region")
    col1, col2 = st.columns([2, 1], gap="medium")

    # Aggregate total sales per region
    region_sales = df.groupby("region")["sales"].sum().reset_index()
    top_region = region_sales.loc[region_sales["sales"].idxmax()]

    # Left: Bar chart (Plotly)
    with col1:
        st.metric("Top Region", f"{top_region['region']} ({top_region['sales']:,})")
        fig3 = px.bar(
            region_sales,
            x="region",
            y="sales",
            title="Total Sales by Region",
            labels={"sales": "Total Sales", "region": "Region"},
        )
        fig3.update_layout(margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig3, use_container_width=True)

    # Right: Heatmap of avg sales by region vs. weekday (Seaborn)
    with col2:
        df["weekday"] = df["date"].dt.day_name()
        heat_data = (
            df.groupby(["region", "weekday"])["sales"]
              .mean()
              .unstack()
              .reindex(columns=[
                  "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
              ])
        )
        overall_avg = df["sales"].mean()
        st.metric("Overall Avg Daily Sale", f"{overall_avg:.2f}")

        fig4, ax4 = plt.subplots(figsize=(6, 4))
        sns.heatmap(
            heat_data,
            annot=True,
            fmt=".1f",
            linewidths=0.5,
            cmap="Blues",
            cbar_kws={"label": "Avg Sales"},
            ax=ax4
        )
        ax4.set_title("Avg Sales by Region and Weekday")
        ax4.set_xlabel("Weekday")
        ax4.set_ylabel("Region")
        plt.xticks(rotation=45)
        st.pyplot(fig4)
