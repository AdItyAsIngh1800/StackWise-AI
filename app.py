import json
import pandas as pd
import streamlit as st

from evaluator.constraints import check_constraints
from evaluator.scoring import calculate_score
from evaluator.explain import explain_winner


@st.cache_data
def load_catalog():
    with open("catalog/options.json", "r") as f:
        return json.load(f)


def main():
    st.title("Referee: ECS vs EKS vs Lambda")
    st.write("Pick options, set weights, and get a side-by-side comparison.")

    catalog = load_catalog()
    options = list(catalog.keys())

    st.header("1) Choose options")
    selected = st.multiselect("Select at least 2:", options, default=["ECS", "EKS"])

    st.header("2) Hard requirement")
    needs_kubernetes = st.checkbox("Need Kubernetes? (Yes/No)", value=False)

    st.header("3) Set weights (higher = more important)")
    weights = {
        "cost": st.slider("cost", 0, 100, 20),
        "ops_simplicity": st.slider("ops_simplicity", 0, 100, 30),
        "scalability": st.slider("scalability", 0, 100, 20),
        "portability": st.slider("portability", 0, 100, 20),
        "time_to_market": st.slider("time_to_market", 0, 100, 10),
    }

    if st.button("Compare"):
        if len(selected) < 2:
            st.error("Please select at least 2 options.")
            return

        results = []
        totals = {}
        breakdowns = {}

        for name in selected:
            data = catalog[name]

            allowed = check_constraints(data, needs_kubernetes)
            if not allowed:
                totals[name] = 0
                breakdowns[name] = {k: 0 for k in data["scores"].keys()}
                results.append({
                    "Option": name,
                    "Allowed": "❌ (Breaks hard requirement)",
                    "Description": data["description"],
                    "Strengths": ", ".join(data["strengths"]),
                    "Weaknesses": ", ".join(data["weaknesses"]),
                    "Total Score": 0
                })
                continue

            total, breakdown = calculate_score(data["scores"], weights)
            totals[name] = total
            breakdowns[name] = breakdown

            results.append({
                "Option": name,
                "Allowed": "✅",
                "Description": data["description"],
                "Strengths": ", ".join(data["strengths"]),
                "Weaknesses": ", ".join(data["weaknesses"]),
                "Total Score": total
            })

        st.subheader("Comparison table")
        df = pd.DataFrame(results).sort_values(by="Total Score", ascending=False)
        st.dataframe(df, use_container_width=True)

        st.subheader("Score breakdown")
        breakdown_df = pd.DataFrame(breakdowns).T
        st.dataframe(breakdown_df, use_container_width=True)

        # Winner: highest total among allowed options
        allowed_totals = {k: v for k, v in totals.items() if v > 0}
        if not allowed_totals:
            st.warning("No option matches your hard requirement. Try changing the requirement.")
            return

        winner = max(allowed_totals, key=allowed_totals.get)
        st.subheader("Trade-off explanation")
        st.success(explain_winner(winner, totals, weights))


if __name__ == "__main__":
    main()