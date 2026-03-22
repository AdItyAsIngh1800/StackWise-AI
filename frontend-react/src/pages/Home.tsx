import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

import API from "../api/client";
import type { RecommendationResponse } from "../types/api";
import Card from "../components/Card";
import LoadingSpinner from "../components/LoadingSpinner";

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
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="space-y-6"
    >
      <section className="rounded-2xl bg-white p-6 shadow-sm dark:bg-gray-800">
        <h1 className="text-3xl font-bold">Build Your Stack</h1>
        <p className="mt-2 text-gray-600 dark:text-gray-300">
          Choose your project requirements and get an explainable recommendation.
        </p>
      </section>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
        <Card>
          <label className="mb-2 block font-medium">Project Type</label>
          <select
            className="w-full rounded border p-2 dark:border-gray-700 dark:bg-gray-900"
            value={projectType}
            onChange={(e) => setProjectType(e.target.value)}
          >
            <option value="api">API</option>
            <option value="web">Web</option>
            <option value="ai-ml">AI/ML</option>
            <option value="enterprise">Enterprise</option>
          </select>
        </Card>

        <Card>
          <label className="mb-2 block font-medium">Expected Scale</label>
          <select
            className="w-full rounded border p-2 dark:border-gray-700 dark:bg-gray-900"
            value={expectedScale}
            onChange={(e) => setExpectedScale(e.target.value)}
          >
            <option value="small">Small</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </Card>

        <Card>
          <label className="mb-2 block font-medium">Team Languages</label>
          <input
            className="w-full rounded border p-2 dark:border-gray-700 dark:bg-gray-900"
            value={teamLanguages.join(",")}
            onChange={(e) =>
              setTeamLanguages(
                e.target.value
                  .split(",")
                  .map((x) => x.trim())
                  .filter(Boolean)
              )
            }
          />
        </Card>

        <Card>
          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={lowOps}
              onChange={(e) => setLowOps(e.target.checked)}
            />
            Prefer managed / low-ops setup
          </label>
        </Card>
      </div>

      {loading && <LoadingSpinner />}

      <button
        onClick={submit}
        disabled={loading}
        className="rounded-lg bg-blue-600 px-6 py-2 text-white hover:bg-blue-700"
      >
        {loading ? "Generating..." : "Get Recommendation"}
      </button>
    </motion.div>
  );
}