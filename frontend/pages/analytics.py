from __future__ import annotations

import requests
import pandas as pd
import streamlit as st

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Analytics Dashboard", layout="wide")

st.title("📊 StackWise Analytics Dashboard")

# ---------------------------
# Top Languages
# ---------------------------
st.header("🔥 Most Recommended Languages")

try:
    res = requests.get(f"{API_BASE_URL}/analytics/top-languages")
    data = res.json()

    df = pd.DataFrame(data)

    if not df.empty:
        st.dataframe(df, use_container_width=True)
        st.bar_chart(df.set_index("language")["count"])
    else:
        st.write("No data available yet.")

except Exception:
    st.error("Failed to load top languages")

st.divider()

# ---------------------------
# Average Confidence
# ---------------------------
st.header("📈 Average Confidence")

try:
    res = requests.get(f"{API_BASE_URL}/analytics/confidence")
    data = res.json()

    value = data.get("average_confidence")

    if value is not None:
        st.metric("Average Confidence", f"{value:.3f}")
        st.progress(value)
    else:
        st.write("No confidence data available")

except Exception:
    st.error("Failed to load confidence")

st.divider()

# ---------------------------
# Recent Runs
# ---------------------------
st.header("🕒 Recent Recommendations")

try:
    res = requests.get(f"{API_BASE_URL}/analytics/recent-runs")
    data = res.json()

    df = pd.DataFrame(data)

    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.write("No recent runs available.")

except Exception:
    st.error("Failed to load recent runs")


st.divider()
st.header("📉 Confidence Trend Over Time")

try:
    res = requests.get(f"{API_BASE_URL}/analytics/confidence-trend")
    data = res.json()

    df = pd.DataFrame(data)

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
        st.line_chart(df.set_index("date")["avg_confidence"])
    else:
        st.write("No trend data available.")

except Exception:
    st.error("Failed to load confidence trend")


st.divider()
st.header("🏆 Top Stack Combinations")

try:
    res = requests.get(f"{API_BASE_URL}/analytics/top-stacks")
    data = res.json()

    df = pd.DataFrame(data)

    if not df.empty:
        st.dataframe(df, use_container_width=True)
        st.bar_chart(df.set_index("language")["count"])
    else:
        st.write("No stack data available.")

except Exception:
    st.error("Failed to load stack combinations")