import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

import API from "../api/client";
import type {
  RecommendationContext,
  RecommendationResponse,
  NaturalLanguageRecommendationResponse,
} from "../types/api";

import Card from "../components/Card";
import SemanticSearchCard from "../components/SemanticSearchCard";

const LANGUAGES = [
  "python",
  "javascript",
  "typescript",
  "java",
  "go",
  "rust",
];

export default function Home() {
  const navigate = useNavigate();

  const [projectType, setProjectType] = useState("api");
  const [expectedScale, setExpectedScale] = useState("medium");
  const [lowOps, setLowOps] = useState(false);
  const [teamLanguages, setTeamLanguages] = useState<string[]>([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [nlQuery, setNlQuery] = useState("");

  function toggleLanguage(lang: string) {
    setTeamLanguages((prev) =>
      prev.includes(lang)
        ? prev.filter((l) => l !== lang)
        : [...prev, lang]
    );
  }

  async function submit() {
    setLoading(true);
    setError(null);

    try {
      const payload: RecommendationContext = {
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

      navigate("/results", {
        state: {
          recommendation: res.data,
          context: payload,
        },
      });
    } catch {
      setError("Failed to fetch recommendation.");
    } finally {
      setLoading(false);
    }
  }

  async function submitNL() {
    if (!nlQuery.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const res = await API.post<NaturalLanguageRecommendationResponse>(
        "/recommend/natural-language",
        { query: nlQuery }
      );

      navigate("/results", {
        state: {
          recommendation: res.data.recommendation,
          context: res.data.parsed_input,
        },
      });
    } catch {
      setError("Failed to process natural language input.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-8"
    >
      <section className="rounded-3xl bg-linear-to-r from-blue-600 via-violet-600 to-fuchsia-600 p-8 text-white shadow-lg">
        <h1 className="text-3xl font-bold">🚀 StackWise-AI</h1>
        <p className="mt-2 text-white/90">
          Intelligent, explainable tech stack recommendations
        </p>
      </section>

      <Card>
        <h2 className="text-lg font-semibold">💬 Natural Language Input</h2>

        <div className="mt-4 flex gap-3">
          <input
            value={nlQuery}
            onChange={(e) => setNlQuery(e.target.value)}
            placeholder="e.g. build scalable API with low ops"
            className="flex-1 rounded-xl border p-3 dark:border-gray-700 dark:bg-gray-900"
          />

          <button
            onClick={submitNL}
            disabled={loading}
            className="rounded-xl bg-linear-to-r from-blue-600 to-violet-600 px-4 py-2 text-white shadow hover:scale-[1.02] disabled:opacity-60"
          >
            Run
          </button>
        </div>
      </Card>

      <SemanticSearchCard />

      <Card>
        <h2 className="text-lg font-semibold">⚙️ Manual Configuration</h2>

        <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2">
          <div>
            <label className="text-sm font-medium">Project Type</label>
            <select
              value={projectType}
              onChange={(e) => setProjectType(e.target.value)}
              className="mt-1 w-full rounded-xl border p-2 dark:border-gray-700 dark:bg-gray-900"
            >
              <option value="api">API</option>
              <option value="web">Web</option>
              <option value="ai-ml">AI/ML</option>
              <option value="enterprise">Enterprise</option>
            </select>
          </div>

          <div>
            <label className="text-sm font-medium">Expected Scale</label>
            <select
              value={expectedScale}
              onChange={(e) => setExpectedScale(e.target.value)}
              className="mt-1 w-full rounded-xl border p-2 dark:border-gray-700 dark:bg-gray-900"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>
        </div>

        <div className="mt-4 flex items-center gap-2">
          <input
            type="checkbox"
            checked={lowOps}
            onChange={(e) => setLowOps(e.target.checked)}
          />
          <label>Prefer low operations / simple setup</label>
        </div>

        <div className="mt-6">
          <label className="text-sm font-medium">Team Languages</label>

          <div className="mt-2 flex flex-wrap gap-2">
            {LANGUAGES.map((lang) => {
              const selected = teamLanguages.includes(lang);

              return (
                <button
                  key={lang}
                  onClick={() => toggleLanguage(lang)}
                  className={`rounded-full px-4 py-2 text-sm transition ${
                    selected
                      ? "bg-linear-to-r from-blue-600 to-violet-600 text-white shadow"
                      : "bg-gray-200 dark:bg-gray-700"
                  }`}
                >
                  {lang}
                </button>
              );
            })}
          </div>
        </div>

        <div className="mt-6">
          <button
            onClick={submit}
            disabled={loading}
            className="w-full rounded-xl bg-linear-to-r from-green-500 to-emerald-500 px-5 py-3 text-white shadow transition hover:scale-[1.02] disabled:opacity-60"
          >
            {loading ? "Running..." : "Get Recommendation"}
          </button>
        </div>

        {error && (
          <div className="mt-4 rounded-xl bg-red-100 p-3 text-red-700 dark:bg-red-900/30 dark:text-red-300">
            {error}
          </div>
        )}
      </Card>
    </motion.div>
  );
}