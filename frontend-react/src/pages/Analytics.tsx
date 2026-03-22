import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import API from "../api/client";
import Card from "../components/Card";

type TopLanguage = {
  winner_language?: string;
  language?: string;
  count: number;
};

type RecentRun = {
  id: number;
  project_type: string;
  winner_language: string;
  score: number;
  created_at: string;
};

type ConfidenceTrendPoint = {
  date: string;
  avg_confidence: number | null;
};

type TopStack = {
  language: string;
  framework: string;
  database: string;
  count: number;
};

export default function Analytics() {
  const [topLanguages, setTopLanguages] = useState<TopLanguage[]>([]);
  const [avgConfidence, setAvgConfidence] = useState<number | null>(null);
  const [recentRuns, setRecentRuns] = useState<RecentRun[]>([]);
  const [confidenceTrend, setConfidenceTrend] = useState<ConfidenceTrendPoint[]>([]);
  const [topStacks, setTopStacks] = useState<TopStack[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadAnalytics() {
      try {
        setLoading(true);
        setError(null);

        const [
          topLanguagesRes,
          avgConfidenceRes,
          recentRunsRes,
          confidenceTrendRes,
          topStacksRes,
        ] = await Promise.all([
          API.get("/analytics/top-languages"),
          API.get("/analytics/confidence"),
          API.get("/analytics/recent-runs"),
          API.get("/analytics/confidence-trend"),
          API.get("/analytics/top-stacks"),
        ]);

        setTopLanguages(topLanguagesRes.data ?? []);
        setAvgConfidence(avgConfidenceRes.data?.average_confidence ?? null);
        setRecentRuns(recentRunsRes.data ?? []);
        setConfidenceTrend(confidenceTrendRes.data ?? []);
        setTopStacks(topStacksRes.data ?? []);
      } catch {
        setError("Failed to load analytics data.");
      } finally {
        setLoading(false);
      }
    }

    loadAnalytics();
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="space-y-6"
    >
      <section className="rounded-2xl bg-white p-6 shadow-sm dark:bg-gray-800">
        <h1 className="text-3xl font-bold">Analytics</h1>
        <p className="mt-2 text-gray-600 dark:text-gray-300">
          View system behavior, recommendation trends, confidence patterns, and
          commonly suggested stack combinations.
        </p>
      </section>

      {loading && (
        <Card>
          <p className="text-gray-600 dark:text-gray-300">Loading analytics...</p>
        </Card>
      )}

      {error && (
        <Card>
          <p className="text-red-600">{error}</p>
        </Card>
      )}

      {!loading && !error && (
        <>
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
            <Card>
              <h2 className="mb-3 text-lg font-semibold">📈 Average Confidence</h2>
              {avgConfidence !== null ? (
                <>
                  <p className="text-3xl font-bold">
                    {avgConfidence.toFixed(3)}
                  </p>
                  <div className="mt-4 h-3 w-full rounded bg-gray-200 dark:bg-gray-700">
                    <div
                      className="h-3 rounded bg-blue-600"
                      style={{ width: `${Math.max(0, Math.min(100, avgConfidence * 100))}%` }}
                    />
                  </div>
                </>
              ) : (
                <p className="text-gray-600 dark:text-gray-300">
                  No confidence data available yet.
                </p>
              )}
            </Card>

            <Card>
              <h2 className="mb-3 text-lg font-semibold">🔥 Most Recommended Languages</h2>
              {topLanguages.length > 0 ? (
                <div className="space-y-2">
                  {topLanguages.map((item, index) => (
                    <div
                      key={`${item.language ?? item.winner_language ?? "lang"}-${index}`}
                      className="flex items-center justify-between rounded border p-3 dark:border-gray-700"
                    >
                      <span>{item.language ?? item.winner_language ?? "-"}</span>
                      <span className="font-semibold">{item.count}</span>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-600 dark:text-gray-300">
                  No recommendation data available yet.
                </p>
              )}
            </Card>
          </div>

          <Card>
            <h2 className="mb-3 text-lg font-semibold">📉 Confidence Trend</h2>
            {confidenceTrend.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="w-full border-collapse text-sm">
                  <thead>
                    <tr>
                      <th className="border p-2 text-left dark:border-gray-700">Date</th>
                      <th className="border p-2 text-left dark:border-gray-700">Average Confidence</th>
                    </tr>
                  </thead>
                  <tbody>
                    {confidenceTrend.map((point) => (
                      <tr key={point.date}>
                        <td className="border p-2 dark:border-gray-700">{point.date}</td>
                        <td className="border p-2 dark:border-gray-700">
                          {point.avg_confidence !== null
                            ? point.avg_confidence.toFixed(3)
                            : "-"}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="text-gray-600 dark:text-gray-300">
                No trend data available yet.
              </p>
            )}
          </Card>

          <Card>
            <h2 className="mb-3 text-lg font-semibold">🏆 Top Stack Combinations</h2>
            {topStacks.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="w-full border-collapse text-sm">
                  <thead>
                    <tr>
                      <th className="border p-2 text-left dark:border-gray-700">Language</th>
                      <th className="border p-2 text-left dark:border-gray-700">Framework</th>
                      <th className="border p-2 text-left dark:border-gray-700">Database</th>
                      <th className="border p-2 text-left dark:border-gray-700">Count</th>
                    </tr>
                  </thead>
                  <tbody>
                    {topStacks.map((stack, index) => (
                      <tr key={`${stack.language}-${stack.framework}-${index}`}>
                        <td className="border p-2 dark:border-gray-700">{stack.language}</td>
                        <td className="border p-2 dark:border-gray-700">{stack.framework}</td>
                        <td className="border p-2 dark:border-gray-700">{stack.database}</td>
                        <td className="border p-2 dark:border-gray-700">{stack.count}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="text-gray-600 dark:text-gray-300">
                No stack combination data available yet.
              </p>
            )}
          </Card>

          <Card>
            <h2 className="mb-3 text-lg font-semibold">🕒 Recent Recommendation Runs</h2>
            {recentRuns.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="w-full border-collapse text-sm">
                  <thead>
                    <tr>
                      <th className="border p-2 text-left dark:border-gray-700">ID</th>
                      <th className="border p-2 text-left dark:border-gray-700">Project Type</th>
                      <th className="border p-2 text-left dark:border-gray-700">Winner</th>
                      <th className="border p-2 text-left dark:border-gray-700">Score</th>
                      <th className="border p-2 text-left dark:border-gray-700">Created At</th>
                    </tr>
                  </thead>
                  <tbody>
                    {recentRuns.map((run) => (
                      <tr key={run.id}>
                        <td className="border p-2 dark:border-gray-700">{run.id}</td>
                        <td className="border p-2 dark:border-gray-700">{run.project_type}</td>
                        <td className="border p-2 dark:border-gray-700">{run.winner_language}</td>
                        <td className="border p-2 dark:border-gray-700">
                          {typeof run.score === "number" ? run.score.toFixed(3) : "-"}
                        </td>
                        <td className="border p-2 dark:border-gray-700">{run.created_at}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="text-gray-600 dark:text-gray-300">
                No recent runs available yet.
              </p>
            )}
          </Card>
        </>
      )}
    </motion.div>
  );
}