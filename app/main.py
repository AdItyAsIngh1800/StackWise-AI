import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000/evaluate"
PARETO_URL = "http://127.0.0.1:8000/pareto"
SAVE_URL = "http://127.0.0.1:8000/scenario/save"

st.set_page_config(page_title="StackWise AI", layout="wide")

st.title("🚀 StackWise AI")
st.caption("Explainable Decision Intelligence Platform for Architecture & Infrastructure Selection")

st.sidebar.header("Configuration")

options = ["ECS", "EKS", "Lambda"]

need_kubernetes = st.sidebar.checkbox("Need Kubernetes")
low_ops_capacity = st.sidebar.checkbox("Low Ops Capacity")
vendor_neutrality = st.sidebar.checkbox("Vendor Neutrality")

cost = st.sidebar.slider("Cost", 0.0, 1.0, 0.2, 0.05)
scalability = st.sidebar.slider("Scalability", 0.0, 1.0, 0.3, 0.05)
portability = st.sidebar.slider("Portability", 0.0, 1.0, 0.2, 0.05)
ops_simplicity = st.sidebar.slider("Ops Simplicity", 0.0, 1.0, 0.15, 0.05)
time_to_market = st.sidebar.slider("Time to Market", 0.0, 1.0, 0.15, 0.05)

weights = {
    "cost": cost,
    "scalability": scalability,
    "portability": portability,
    "ops_simplicity": ops_simplicity,
    "time_to_market": time_to_market,
}

payload = {
    "options": options,
    "constraints": {
        "need_kubernetes": need_kubernetes,
        "low_ops_capacity": low_ops_capacity,
        "vendor_neutrality": vendor_neutrality,
    },
    "weights": weights,
}

if st.sidebar.button("Evaluate"):
    try:
        response = requests.post(API_URL, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        if not data["ranked_options"]:
            st.error(data["explanation"])
            st.stop()

        st.subheader("Winner")
        st.success(f"{data['winner']}")

        st.subheader("Explanation")
        st.write(data["explanation"])

        ranked_df = pd.DataFrame(data["ranked_options"])
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Ranked Options")
            st.dataframe(ranked_df, use_container_width=True)

        with col2:
            fig = px.bar(
                ranked_df,
                x="name",
                y="score",
                text="score",
                title="Final Scores"
            )
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Sensitivity Analysis")
        sens_df = pd.DataFrame(
            [{"criterion": k, "winner_after_increase": v} for k, v in data["sensitivity"].items()]
        )
        st.dataframe(sens_df, use_container_width=True)

        fig2 = px.bar(
            sens_df,
            x="criterion",
            y=[1] * len(sens_df),
            color="winner_after_increase",
            title="Winner Changes Under Weight Perturbation"
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Confidence")
        confidence = float(data["confidence"])
        st.progress(min(max(confidence, 0.0), 1.0))
        st.metric("Confidence Score", f"{confidence:.3f}")

        st.subheader("Pareto View")
        pareto_response = requests.get(PARETO_URL, timeout=30)
        pareto_response.raise_for_status()
        pareto_data = pareto_response.json()["pareto_frontier"]
        pareto_df = pd.DataFrame(pareto_data)

        st.dataframe(pareto_df, use_container_width=True)

        if not pareto_df.empty:
            fig3 = px.scatter(
                pareto_df,
                x="ops_simplicity",
                y="scalability",
                text="name",
                size="cost",
                title="Pareto Trade-off: Ops Simplicity vs Scalability"
            )
            st.plotly_chart(fig3, use_container_width=True)

        if st.button("Save Scenario"):
            save_resp = requests.post(
                SAVE_URL,
                json={"payload": payload, "result": data},
                timeout=30,
            )
            save_resp.raise_for_status()
            scenario_id = save_resp.json()["scenario_id"]
            st.success(f"Scenario saved: {scenario_id}")

    except requests.RequestException as e:
        st.error(f"API request failed: {e}")