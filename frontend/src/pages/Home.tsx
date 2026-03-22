import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

import API from "../api/client";
import type { RecommendationResponse } from "../types/api";

import Card from "../components/Card";
import LoadingSpinner from "../components/LoadingSpinner";
import LanguageSelector from "../components/LanguageSelector";

export default function Home() {
  const navigate = useNavigate();

  const [projectType, setProjectType] = useState("api");
  const [teamLanguages, setTeamLanguages] = useState<string[]>(["python"]);
  const [lowOps, setLowOps] = useState(true);
  const [expectedScale, setExpectedScale] = useState("medium");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submit() {
    setLoading(true);
    setError(null);

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
      setError("Failed to fetch recommendation. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="space-y-8"
    >
      <section className="rounded-3xl bg-linear-to-r from-blue-600 via-violet-600 to-fuchsia-600 p-8 text-white shadow-lg">
        <div className="max-w-3xl space-y-4">
          <span className="inline-flex rounded-full bg-white/15 px-3 py-1 text-sm backdrop-blur">
            Decision Intelligence for Tech Stacks
          </span>

          <h1 className="text-4xl font-bold md:text-5xl">
            Choose the right stack with confidence
          </h1>

          <p className="text-white/90">
            Compare technologies using scoring, trade-offs, and system-level
            reasoning — not guesswork.
          </p>
        </div>
      </section>

      <section className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <div className="rounded-2xl bg-blue-50 p-5 shadow-sm dark:bg-blue-950/30">
          <h3 className="font-semibold">⚡ Fast Decisions</h3>
          <p className="text-sm text-gray-600 dark:text-gray-300">
            Get recommendations instantly based on your constraints.
          </p>
        </div>

        <div className="rounded-2xl bg-violet-50 p-5 shadow-sm dark:bg-violet-950/30">
          <h3 className="font-semibold">📊 Explainable</h3>
          <p className="text-sm text-gray-600 dark:text-gray-300">
            Understand why a stack is chosen.
          </p>
        </div>

        <div className="rounded-2xl bg-fuchsia-50 p-5 shadow-sm dark:bg-fuchsia-950/30">
          <h3 className="font-semibold">⚖️ Trade-offs</h3>
          <p className="text-sm text-gray-600 dark:text-gray-300">
            Compare alternatives using Pareto analysis.
          </p>
        </div>
      </section>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
        <Card>
          <label className="mb-2 block font-medium">Project Type</label>
          <select
            className="w-full rounded-xl border p-3 dark:border-gray-700 dark:bg-gray-900"
            value={projectType}
            onChange={(e) => setProjectType(e.target.value)}
          >
            <option value="api">API</option>
            <option value="web">Web</option>
            <option value="ai-ml">AI/ML</option>
            <option value="enterprise">Enterprise</option>
          </select>
          <p className="mt-2 text-sm text-gray-500 dark:text-gray-300">
            Select the primary type of system you are planning to build.
          </p>
        </Card>

        <Card>
          <label className="mb-2 block font-medium">Expected Scale</label>
          <select
            className="w-full rounded-xl border p-3 dark:border-gray-700 dark:bg-gray-900"
            value={expectedScale}
            onChange={(e) => setExpectedScale(e.target.value)}
          >
            <option value="small">Small</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
          <p className="mt-2 text-sm text-gray-500 dark:text-gray-300">
            Small for side projects, medium for standard production systems, high
            for enterprise or large-scale workloads.
          </p>
        </Card>

        <Card>
          <label className="mb-2 block font-medium">Team Languages</label>
          <LanguageSelector value={teamLanguages} onChange={setTeamLanguages} />
          <p className="mt-2 text-sm text-gray-500 dark:text-gray-300">
            Select one or more languages your team is comfortable with.
          </p>
        </Card>

        <Card>
          <label className="flex items-center gap-2 font-medium">
            <input
              type="checkbox"
              checked={lowOps}
              onChange={(e) => setLowOps(e.target.checked)}
            />
            Prefer low-ops / managed setup
          </label>
          <p className="mt-2 text-sm text-gray-500 dark:text-gray-300">
            Better for faster delivery and reduced infrastructure maintenance.
          </p>
        </Card>
      </div>

      {loading && <LoadingSpinner />}

      {error && (
        <div className="rounded-xl bg-red-100 p-3 text-red-700 dark:bg-red-900/30 dark:text-red-300">
          {error}
        </div>
      )}

      <div className="flex flex-wrap items-center gap-4">
        <button
          onClick={submit}
          disabled={loading}
          className="rounded-xl bg-linear-to-r from-blue-600 to-violet-600 px-6 py-3 text-white shadow transition hover:scale-[1.02] hover:shadow-lg disabled:opacity-60"
        >
          {loading ? "Generating..." : "Get Recommendation"}
        </button>

        <span className="text-sm text-gray-500 dark:text-gray-300">
          Powered by weighted scoring, evidence signals, confidence, and trade-off analysis.
        </span>
      </div>
    </motion.div>
  );
}