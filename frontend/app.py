from __future__ import annotations

import requests
import streamlit as st

API_BASE_URL = "http://127.0.0.1:8000"
RECOMMEND_URL = f"{API_BASE_URL}/recommend"
HEALTH_URL = f"{API_BASE_URL}/health"
SCENARIOS_URL = f"{API_BASE_URL}/scenarios"

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


st.title("🚀 StackWise-AI")
st.subheader("AI-Powered Tech Stack Recommendation System")

backend_ok = check_backend_health()

if backend_ok:
    st.success("Backend is connected")
else:
    st.error("Backend is not running. Start FastAPI with: uvicorn backend.main:app --reload")


st.sidebar.header("Project Inputs")

scenario_name = st.sidebar.text_input("Scenario Name (optional)")

project_type = st.sidebar.selectbox(
    "Project Type",
    ["api", "web", "ai-ml", "enterprise"],
)

team_languages = st.sidebar.multiselect(
    "Team Known Languages",
    ["python", "javascript", "typescript", "java", "go", "rust", "csharp"],
)

expected_scale = st.sidebar.selectbox(
    "Expected Scale",
    ["small", "medium", "high"],
)

low_ops = st.sidebar.checkbox("Prefer Low Ops / Managed Experience")
prefer_enterprise = st.sidebar.checkbox("Enterprise Preference")
prototype_only = st.sidebar.checkbox("Prototype Only")
rapid_schema_changes = st.sidebar.checkbox("Rapid Schema Changes")
needs_cache = st.sidebar.checkbox("Needs Caching")
prefer_portability = st.sidebar.checkbox("Prefer Portability")

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

if st.sidebar.button("Get Recommendation"):
    if not backend_ok:
        st.error("Cannot request recommendation because backend is not running.")
        st.stop()

    try:
        query_params = {}
        if scenario_name.strip():
            query_params["scenario_name"] = scenario_name.strip()

        response = requests.post(
            RECOMMEND_URL,
            params=query_params,
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        st.header("🏆 Recommended Stack")

        winner = data.get("winner")
        if winner:
            col1, col2 = st.columns(2)

            with col1:
                st.success(f"Language: {winner['language']}")
                st.write(f"**Score:** {round(winner['score'], 3)}")
                st.write(f"**Backend Framework:** {winner['backend_framework']}")
                st.write(f"**Database:** {winner['database']}")
                st.write(f"**Deployment:** {winner['deployment']}")

            with col2:
                st.info(
                    "Primary recommendation generated from project fit, "
                    "team fit, ops fit, ecosystem evidence, and stability checks."
                )
        else:
            st.warning("No recommendation could be generated.")

        st.header("📈 Confidence Score")
        confidence = data.get("confidence", 0.0)
        st.metric("Confidence", confidence)

        st.header("🔍 Sensitivity Analysis")
        sensitivity = data.get("sensitivity", {})

        if sensitivity:
            st.write(f"**Base Winner:** {sensitivity.get('base_winner')}")
            st.write(f"**Stability Score:** {sensitivity.get('stability')}")

            variations = sensitivity.get("variations", [])
            if variations:
                for variation in variations:
                    st.write(
                        f"- **{variation['scenario']}** → {variation['winner']}"
                    )
            else:
                st.write("No sensitivity variations available.")
        else:
            st.write("No sensitivity analysis available.")

        st.header("🔄 Alternatives")
        alternatives = data.get("alternatives", [])

        if alternatives:
            for alt in alternatives:
                st.info(
                    f"{alt['language']} | "
                    f"Score: {round(alt['score'], 3)} | "
                    f"Framework: {alt['backend_framework']} | "
                    f"DB: {alt['database']} | "
                    f"Deployment: {alt['deployment']}"
                )
        else:
            st.write("No alternatives available.")

        st.header("📊 Language Ranking")
        ranked = data.get("ranked_languages", [])

        if ranked:
            chart_rows = {
                "Language": [item["language"] for item in ranked],
                "Score": [item["score"] for item in ranked],
            }
            st.bar_chart(chart_rows, x="Language", y="Score")
        else:
            st.write("No ranking data available.")

        st.header("🧠 Explanation")
        st.write(data.get("explanation", "No explanation available."))

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
    except Exception as exc:
        st.error(f"Unexpected error: {exc}")


st.header("📁 Saved Scenarios")

if backend_ok:
    scenarios = load_scenarios()

    if scenarios:
        for sc in scenarios:
            scenario_label = sc["scenario_name"] if sc["scenario_name"] else "(no name)"
            st.write(
                f"**ID:** {sc['id']} | "
                f"**Scenario:** {scenario_label} | "
                f"**Project Type:** {sc['project_type']} | "
                f"**Created At:** {sc['created_at']}"
            )
    else:
        st.write("No saved scenarios found yet.")
else:
    st.write("Scenarios are unavailable because the backend is offline.")