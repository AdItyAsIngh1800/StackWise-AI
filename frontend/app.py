from __future__ import annotations

import pandas as pd
import requests
import streamlit as st

API_BASE_URL = "http://127.0.0.1:8000"
RECOMMEND_URL = f"{API_BASE_URL}/recommend"
HEALTH_URL = f"{API_BASE_URL}/health"
SCENARIOS_URL = f"{API_BASE_URL}/scenarios"
SCENARIO_DETAIL_URL = f"{API_BASE_URL}/scenario"

st.set_page_config(page_title="StackWise-AI", layout="wide")


def check_backend_health() -> bool:
    try:
        response = requests.get(HEALTH_URL, timeout=3)
        response.raise_for_status()
        data = response.json()
        return data.get("status") == "ok"
    except requests.RequestException:
        return False


def load_scenarios() -> list[dict]:
    try:
        response = requests.get(SCENARIOS_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data if isinstance(data, list) else []
    except requests.RequestException:
        return []


def load_scenario_detail(scenario_id: int) -> dict | None:
    try:
        response = requests.get(f"{SCENARIO_DETAIL_URL}/{scenario_id}", timeout=5)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict) and "error" not in data:
            return data
        return None
    except requests.RequestException:
        return None


def confidence_label(value: float) -> str:
    if value >= 0.75:
        return "High"
    if value >= 0.5:
        return "Moderate"
    return "Low"


def build_summary_text(winner: dict | None) -> str:
    if not winner:
        return "No recommendation could be generated."

    return (
        f"Recommended stack: {winner['language']} + "
        f"{winner['backend_framework']} + {winner['database']} + "
        f"{winner['deployment']}."
    )


backend_ok = check_backend_health()

# -----------------------------
# Header / Hero
# -----------------------------
st.title("🚀 StackWise-AI")
st.caption(
    "Explainable decision-support system for selecting a suitable tech stack "
    "based on project needs, team familiarity, ecosystem evidence, and trade-offs."
)

if backend_ok:
    st.success("Backend status: Connected")
else:
    st.error("Backend status: Offline. Start FastAPI with: uvicorn backend.main:app --reload")

st.divider()

# -----------------------------
# Sidebar Inputs
# -----------------------------
st.sidebar.header("Project Profile")

st.sidebar.subheader("Context")
scenario_name = st.sidebar.text_input("Scenario Name", help="Optional name for saving this recommendation run.")
project_type = st.sidebar.selectbox(
    "Project Type",
    ["api", "web", "ai-ml", "enterprise"],
    help="Primary type of project you are building.",
)
expected_scale = st.sidebar.selectbox(
    "Expected Scale",
    ["small", "medium", "high"],
    help="Small = side project/internal app, medium = startup/production app, high = large-scale or enterprise workload.",
)

st.sidebar.subheader("Team")
team_languages = st.sidebar.multiselect(
    "Team Known Languages",
    ["python", "javascript", "typescript", "java", "go", "rust", "csharp"],
    help="Languages your team is already comfortable using.",
)

st.sidebar.subheader("Preferences")
low_ops = st.sidebar.checkbox("Prefer managed / low-ops setup")
prefer_enterprise = st.sidebar.checkbox("Enterprise preference")
prototype_only = st.sidebar.checkbox("Prototype / MVP stage")
rapid_schema_changes = st.sidebar.checkbox("Rapid schema changes expected")
needs_cache = st.sidebar.checkbox("Caching / real-time performance needed")
prefer_portability = st.sidebar.checkbox("Prefer portability")

payload = {
    "project_type": project_type,
    "team_languages": team_languages,
    "low_ops": low_ops,
    "expected_scale": expected_scale,
    "prefer_enterprise": prefer_enterprise,
    "prototype_only": prototype_only,
    "rapid_schema_changes": rapid_schema_changes,
    "needs_cache": needs_cache,
    "prefer_portability": prefer_portability,
}

if not team_languages:
    st.sidebar.info("No team languages selected. Recommendation will rely more on ecosystem evidence.")

if prototype_only and expected_scale == "high":
    st.sidebar.warning("Prototype mode and high scale can conflict. Results may emphasize trade-offs.")

run_clicked = st.sidebar.button("Get Recommendation", use_container_width=True)

# -----------------------------
# Main Result Area
# -----------------------------
if run_clicked:
    if not backend_ok:
        st.error("Cannot request recommendation because backend is not running.")
        st.stop()

    try:
        query_params = {}
        if scenario_name.strip():
            query_params["scenario_name"] = scenario_name.strip()

        with st.spinner("Generating recommendation..."):
            response = requests.post(
                RECOMMEND_URL,
                params=query_params,
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

        winner = data.get("winner")
        alternatives = data.get("alternatives", [])
        ranked = data.get("ranked_languages", [])
        confidence = float(data.get("confidence", 0.0))
        sensitivity = data.get("sensitivity", {})
        pareto = data.get("pareto", [])
        why_not = data.get("why_not", [])
        explanation = data.get("explanation", "No explanation available.")

        # -----------------------------
        # Summary
        # -----------------------------
        st.header("🏆 Recommendation Summary")
        st.write(build_summary_text(winner))

        if winner:
            st.header("📌 Final Decision")
            team_text = ", ".join(team_languages) if team_languages else "multiple possible stacks"
            st.success(
                f"""
Recommended: {winner['language']} stack

Best suited for:
- {project_type} projects
- {expected_scale} scale
- team familiar with {team_text}
"""
            )

            col1, col2 = st.columns([1.2, 1])

            with col1:
                st.subheader("Primary Recommendation")
                st.success(f"Language: {winner['language']}")
                st.write(f"**Backend Framework:** {winner['backend_framework']}")
                st.write(f"**Database:** {winner['database']}")
                st.write(f"**Deployment:** {winner['deployment']}")
                st.write(f"**Score:** {round(winner['score'], 3)}")

            with col2:
                st.subheader("Confidence")
                st.metric("Confidence Score", f"{confidence:.3f}")
                st.progress(max(0.0, min(confidence, 1.0)))
                st.write(f"**Confidence Level:** {confidence_label(confidence)}")

        st.divider()

        # -----------------------------
        # Alternatives
        # -----------------------------
        st.header("🔄 Alternatives")
        if alternatives:
            cols = st.columns(len(alternatives)) if len(alternatives) <= 3 else st.columns(3)

            for idx, alt in enumerate(alternatives):
                with cols[idx % len(cols)]:
                    st.info(
                        f"**{alt['language']}**\n\n"
                        f"Score: {round(alt['score'], 3)}\n\n"
                        f"Framework: {alt['backend_framework']}\n\n"
                        f"Database: {alt['database']}\n\n"
                        f"Deployment: {alt['deployment']}"
                    )
        else:
            st.write("No alternatives available.")

        st.divider()

        # -----------------------------
        # Ranking
        # -----------------------------
        st.header("📊 Language Ranking")
        if ranked:
            ranked_df = pd.DataFrame(ranked)
            st.dataframe(ranked_df, use_container_width=True)
            st.bar_chart(ranked_df.set_index("language")["score"])
        else:
            st.write("No ranking data available.")

        st.divider()

        # -----------------------------
        # Sensitivity
        # -----------------------------
        st.header("🔍 Sensitivity Analysis")
        if sensitivity:
            top_left, top_right = st.columns(2)
            with top_left:
                st.write(f"**Base Winner:** {sensitivity.get('base_winner')}")
            with top_right:
                st.write(f"**Stability Score:** {sensitivity.get('stability')}")

            variations = sensitivity.get("variations", [])
            if variations:
                sens_df = pd.DataFrame(variations)
                st.dataframe(sens_df, use_container_width=True)
            else:
                st.write("No sensitivity variations available.")
        else:
            st.write("No sensitivity analysis available.")

        st.divider()

        # -----------------------------
        # Pareto
        # -----------------------------
        st.header("⚖️ Pareto Optimal Options")
        if pareto:
            pareto_df = pd.DataFrame(pareto)
            st.dataframe(pareto_df, use_container_width=True)
            if {"ecosystem", "score"}.issubset(set(pareto_df.columns)):
                st.scatter_chart(
                    pareto_df,
                    x="ecosystem",
                    y="score",
                )
        else:
            st.write("No Pareto optimal options found.")

        st.divider()

        # -----------------------------
        # Why Not Selected
        # -----------------------------
        st.header("❌ Why Not Selected")
        if why_not:
            why_not_df = pd.DataFrame(why_not)
            st.dataframe(why_not_df, use_container_width=True)
        else:
            st.write("No comparison insights available.")

        st.divider()

        # -----------------------------
        # Explanation
        # -----------------------------
        st.header("🧠 Explanation")
        st.write(explanation)

    except requests.exceptions.ConnectionError:
        st.error("Backend connection failed. Start FastAPI with: uvicorn backend.main:app --reload")
    except requests.exceptions.Timeout:
        st.error("The backend request timed out.")
    except requests.exceptions.HTTPError as exc:
        try:
            detail = exc.response.json()
        except Exception:
            detail = exc.response.text if exc.response is not None else str(exc)
        st.error(f"Backend returned an error: {detail}")
    except Exception:
        st.error("Something went wrong while generating the recommendation. Please try again.")

st.divider()

# -----------------------------
# Saved Scenarios
# -----------------------------
st.header("📁 Saved Scenarios")

if backend_ok:
    scenarios = load_scenarios()

    if scenarios:
        scenarios_df = pd.DataFrame(scenarios)
        st.dataframe(scenarios_df, use_container_width=True)

        st.subheader("Reload Scenario")
        scenario_ids = [int(x) for x in scenarios_df["id"].dropna().tolist()]

        if scenario_ids:
            selected_id = st.selectbox(
                "Select Scenario ID",
                options=scenario_ids,
            )

            if st.button("Load Scenario Details"):
                scenario_detail = load_scenario_detail(selected_id)
                if scenario_detail:
                    st.json(scenario_detail)
                else:
                    st.warning("Could not load scenario details.")
        else:
            st.warning("No valid scenario IDs found.")
    else:
        st.write("No saved scenarios found yet.")
else:
    st.write("Scenarios are unavailable because the backend is offline.")