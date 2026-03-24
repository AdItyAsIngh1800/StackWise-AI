import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  LineChart,
  Line,
  Cell,
} from "recharts";

import API from "../api/client";
import Card from "../components/Card";
import type {
  TopLanguage,
  RecentRun,
  ConfidenceTrendPoint,
  ProjectTypeDistribution,
} from "../types/api";

const BAR_COLORS = [
  "#2563eb",
  "#7c3aed",
  "#db2777",
  "#10b981",
  "#f59e0b",
  "#ef4444",
];

function AnalyticsSkeleton() {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
        {[1, 2, 3].map((i) => (
          <div
            key={i}
            className="animate-pulse rounded-2xl bg-gray-200 p-10 dark:bg-gray-700"
          />
        ))}
      </div>

      {[1, 2, 3, 4].map((i) => (
        <div
          key={i}
          className="animate-pulse space-y-3 rounded-2xl bg-white p-6 shadow-sm dark:bg-gray-800"
        >
          <div className="h-6 w-1/3 rounded bg-gray-300 dark:bg-gray-600" />
          <div className="h-48 rounded bg-gray-200 dark:bg-gray-700" />
        </div>
      ))}
    </div>
  );
}

export default function Analytics() {
  const [topLanguages, setTopLanguages] = useState<TopLanguage[]>([]);
  const [avgConfidence, setAvgConfidence] = useState<number | null>(null);
  const [recentRuns, setRecentRuns] = useState<RecentRun[]>([]);
  const [confidenceTrend, setConfidenceTrend] = useState<ConfidenceTrendPoint[]>(
    []
  );
  const [projectTypes, setProjectTypes] = useState<ProjectTypeDistribution[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [langs, conf, runs, trend, types] = await Promise.all([
          API.get<TopLanguage[]>("/analytics/top-languages"),
          API.get<{ average_confidence: number | null }>("/analytics/confidence"),
          API.get<RecentRun[]>("/analytics/recent-runs"),
          API.get<ConfidenceTrendPoint[]>("/analytics/confidence-trend"),
          API.get<ProjectTypeDistribution[]>("/analytics/project-types"),
        ]);

        setTopLanguages(langs.data);
        setAvgConfidence(conf.data.average_confidence);
        setRecentRuns(runs.data);
        setConfidenceTrend(trend.data);
        setProjectTypes(types.data);
      } finally {
        setLoading(false);
      }
    }

    load();
  }, []);

  const topLanguagesChartData = topLanguages.map((item) => ({
    language: item.language ?? item.winner_language ?? "Unknown",
    count: item.count,
  }));

  const recentRunsChartData = recentRuns.map((run) => ({
    id: String(run.id),
    score: run.score,
    winner_language: run.winner_language,
  }));

  const confidenceTrendChartData = confidenceTrend.map((point) => ({
    date: point.date,
    avg_confidence: point.avg_confidence ?? 0,
  }));

  const projectTypeChartData = projectTypes.map((item) => ({
    project_type: item.project_type,
    count: item.count,
  }));

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-8"
    >
      <section className="rounded-3xl bg-linear-to-r from-blue-600 via-violet-600 to-fuchsia-600 p-8 text-white shadow-lg">
        <h1 className="text-3xl font-bold">Analytics Dashboard</h1>
        <p className="mt-2 text-white/90">
          Insights from recommendation engine behavior and trends.
        </p>
      </section>

      {loading && <AnalyticsSkeleton />}

      {!loading && (
        <>
          <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
            <div className="rounded-2xl bg-blue-500 p-5 text-white shadow transition hover:scale-[1.02] hover:shadow-lg">
              <p className="text-sm opacity-80">Average Confidence</p>
              <h2 className="text-2xl font-bold">
                {avgConfidence !== null ? avgConfidence.toFixed(3) : "-"}
              </h2>
            </div>

            <div className="rounded-2xl bg-violet-500 p-5 text-white shadow transition hover:scale-[1.02] hover:shadow-lg">
              <p className="text-sm opacity-80">Total Runs</p>
              <h2 className="text-2xl font-bold">{recentRuns.length}</h2>
            </div>

            <div className="rounded-2xl bg-fuchsia-500 p-5 text-white shadow transition hover:scale-[1.02] hover:shadow-lg">
              <p className="text-sm opacity-80">Tracked Project Types</p>
              <h2 className="text-2xl font-bold">{projectTypes.length}</h2>
            </div>
          </div>

          <Card>
            <h3 className="mb-3 text-lg font-semibold">🔥 Most Used Languages</h3>
            <p className="mb-4 text-sm text-gray-500 dark:text-gray-300">
              Shows how often each language was selected across recommendations.
            </p>

            <div style={{ width: "100%", height: 320 }}>
              <ResponsiveContainer>
                <BarChart data={topLanguagesChartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#cbd5e1" />
                  <XAxis dataKey="language" stroke="#64748b" />
                  <YAxis stroke="#64748b" />
                  <Tooltip
                    formatter={(value) => [String(value), "Count"]}
                    contentStyle={{
                      backgroundColor: "#111827",
                      border: "none",
                      borderRadius: "12px",
                      color: "#ffffff",
                    }}
                  />
                  <Bar dataKey="count" radius={[8, 8, 0, 0]}>
                    {topLanguagesChartData.map((entry, index) => (
                      <Cell
                        key={`cell-${entry.language}`}
                        fill={BAR_COLORS[index % BAR_COLORS.length]}
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </Card>

          <Card>
            <h3 className="mb-3 text-lg font-semibold">📉 Confidence Trend</h3>
            <p className="mb-4 text-sm text-gray-500 dark:text-gray-300">
              Tracks how average confidence changes across saved recommendation runs.
            </p>

            <div style={{ width: "100%", height: 320 }}>
              <ResponsiveContainer>
                <LineChart data={confidenceTrendChartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#cbd5e1" />
                  <XAxis dataKey="date" stroke="#64748b" />
                  <YAxis domain={[0, 1]} stroke="#64748b" />
                  <Tooltip
                    formatter={(value) => [
                      typeof value === "number" ? value.toFixed(3) : String(value),
                      "Avg Confidence",
                    ]}
                    contentStyle={{
                      backgroundColor: "#111827",
                      border: "none",
                      borderRadius: "12px",
                      color: "#ffffff",
                    }}
                  />
                  <Line
                    type="monotone"
                    dataKey="avg_confidence"
                    stroke="#7c3aed"
                    strokeWidth={3}
                    dot={{ r: 5 }}
                    activeDot={{ r: 7 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </Card>

          <Card>
            <h3 className="mb-3 text-lg font-semibold">📦 Project Type Distribution</h3>
            <p className="mb-4 text-sm text-gray-500 dark:text-gray-300">
              Shows which kinds of projects are most frequently evaluated.
            </p>

            <div style={{ width: "100%", height: 320 }}>
              <ResponsiveContainer>
                <BarChart data={projectTypeChartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#cbd5e1" />
                  <XAxis dataKey="project_type" stroke="#64748b" />
                  <YAxis stroke="#64748b" />
                  <Tooltip
                    formatter={(value) => [String(value), "Count"]}
                    contentStyle={{
                      backgroundColor: "#111827",
                      border: "none",
                      borderRadius: "12px",
                      color: "#ffffff",
                    }}
                  />
                  <Bar dataKey="count" radius={[8, 8, 0, 0]}>
                    {projectTypeChartData.map((entry, index) => (
                      <Cell
                        key={`cell-${entry.project_type}`}
                        fill={BAR_COLORS[index % BAR_COLORS.length]}
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </Card>

          <Card>
            <h3 className="mb-3 text-lg font-semibold">🕒 Recent Run Scores</h3>
            <p className="mb-4 text-sm text-gray-500 dark:text-gray-300">
              Compares scores of the most recent recommendation runs.
            </p>

            <div style={{ width: "100%", height: 320 }}>
              <ResponsiveContainer>
                <BarChart data={recentRunsChartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#cbd5e1" />
                  <XAxis dataKey="id" stroke="#64748b" />
                  <YAxis domain={[0, 1]} stroke="#64748b" />
                  <Tooltip
                    formatter={(value) => [
                      typeof value === "number" ? value.toFixed(3) : String(value),
                      "Score",
                    ]}
                    labelFormatter={(label, payload) => {
                      const lang = payload?.[0]?.payload?.winner_language;
                      return `Run ${label}${lang ? ` • ${lang}` : ""}`;
                    }}
                    contentStyle={{
                      backgroundColor: "#111827",
                      border: "none",
                      borderRadius: "12px",
                      color: "#ffffff",
                    }}
                  />
                  <Bar dataKey="score" radius={[8, 8, 0, 0]}>
                    {recentRunsChartData.map((entry, index) => (
                      <Cell
                        key={`cell-${entry.id}`}
                        fill={BAR_COLORS[index % BAR_COLORS.length]}
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </>
      )}
    </motion.div>
  );
}