import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api/client";
import type { RecommendationResponse } from "../types/api";

export default function Home() {
  const navigate = useNavigate();

  const [projectType, setProjectType] = useState("api");
  const [teamLanguages, setTeamLanguages] = useState<string[]>(["python"]);
  const [lowOps, setLowOps] = useState(true);
  const [expectedScale, setExpectedScale] = useState("medium");
  const [loading, setLoading] = useState(false);

  async function submit() {
    setLoading(true);
    try {
      const payload = {
        project_type: projectType,
        team_languages: teamLanguages,
        low_ops: lowOps,
        expected_scale: expectedScale,
        prefer_enterprise: false,
        prototype_only: false,
        rapid_schema_changes: false,
        needs_cache: false,
        prefer_portability: false,
      };

      const res = await API.post<RecommendationResponse>("/recommend", payload);
      navigate("/results", { state: res.data });
    } catch {
      alert("Failed to fetch recommendation.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <h1>StackWise-AI</h1>
      <p>Explainable tech stack decision support system.</p>

      <div>
        <label>Project Type </label>
        <select value={projectType} onChange={(e) => setProjectType(e.target.value)}>
          <option value="api">API</option>
          <option value="web">Web</option>
          <option value="ai-ml">AI/ML</option>
          <option value="enterprise">Enterprise</option>
        </select>
      </div>

      <div style={{ marginTop: 12 }}>
        <label>Expected Scale </label>
        <select value={expectedScale} onChange={(e) => setExpectedScale(e.target.value)}>
          <option value="small">Small</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </div>

      <div style={{ marginTop: 12 }}>
        <label>
          <input
            type="checkbox"
            checked={lowOps}
            onChange={(e) => setLowOps(e.target.checked)}
          />
          Prefer low ops
        </label>
      </div>

      <div style={{ marginTop: 12 }}>
        <label>Team Languages (comma-separated)</label>
        <input
          value={teamLanguages.join(",")}
          onChange={(e) =>
            setTeamLanguages(
              e.target.value
                .split(",")
                .map((x) => x.trim())
                .filter(Boolean)
            )
          }
          style={{ display: "block", width: 320 }}
        />
      </div>

      <button onClick={submit} disabled={loading} style={{ marginTop: 16 }}>
        {loading ? "Generating..." : "Get Recommendation"}
      </button>
    </div>
  );
}