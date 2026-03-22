import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import API from "../api/client";
import Card from "../components/Card";

type TopLanguage = {
  language?: string;
  winner_language?: string;
  count: number;
};

type RecentRun = {
  id: number;
  project_type: string;
  winner_language: string;
  score: number;
  created_at: string;
};

const LANGUAGE_ICONS: Record<string, string> = {
  python: "🐍",
  javascript: "⚡",
  typescript: "🟦",
  java: "☕",
  go: "🐹",
  "c++": "💠",
  rust: "🦀",
  "c#": "🎯",
  php: "🐘",
};

function getLanguageLabel(item: TopLanguage): string {
  return item.language ?? item.winner_language ?? "Unknown";
}

function getLanguageDisplay(name: string): string {
  const icon = LANGUAGE_ICONS[name.toLowerCase()] ?? "🔹";
  return `${icon} ${name}`;
}

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

      {[1, 2].map((i) => (
        <div
          key={i}
          className="animate-pulse space-y-3 rounded-2xl bg-white p-6 shadow-sm dark:bg-gray-800"
        >
          <div className="h-6 w-1/3 rounded bg-gray-300 dark:bg-gray-600" />
          <div className="h-4 rounded bg-gray-200 dark:bg-gray-700" />
          <div className="h-4 rounded bg-gray-200 dark:bg-gray-700" />
          <div className="h-4 w-2/3 rounded bg-gray-200 dark:bg-gray-700" />
        </div>
      ))}
    </div>
  );
}

export default function Analytics() {
  const [topLanguages, setTopLanguages] = useState<TopLanguage[]>([]);
  const [avgConfidence, setAvgConfidence] = useState<number | null>(null);
  const [recentRuns, setRecentRuns] = useState<RecentRun[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [langs, conf, runs] = await Promise.all([
          API.get<TopLanguage[]>("/analytics/top-languages"),
          API.get<{ average_confidence: number | null }>("/analytics/confidence"),
          API.get<RecentRun[]>("/analytics/recent-runs"),
        ]);

        setTopLanguages(langs.data);
        setAvgConfidence(conf.data.average_confidence);
        setRecentRuns(runs.data);
      } finally {
        setLoading(false);
      }
    }

    load();
  }, []);

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
              <p className="text-sm opacity-80">Top Language</p>
              <h2 className="text-2xl font-bold">
                {topLanguages.length > 0
                  ? getLanguageDisplay(getLanguageLabel(topLanguages[0]))
                  : "-"}
              </h2>
            </div>
          </div>

          <Card>
            <h3 className="mb-3 font-semibold">🔥 Most Used Languages</h3>

            {topLanguages.length > 0 ? (
              <div className="space-y-2">
                {topLanguages.map((lang, i) => {
                  const label = getLanguageLabel(lang);
                  return (
                    <div
                      key={`${label}-${i}`}
                      className="flex justify-between rounded border p-3 transition hover:scale-[1.01] hover:shadow-sm dark:border-gray-700"
                    >
                      <span>{getLanguageDisplay(label)}</span>
                      <span className="font-semibold">{lang.count}</span>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="py-10 text-center text-gray-500 dark:text-gray-300">
                <p className="text-lg">No analytics data yet</p>
                <p className="text-sm">
                  Run a few recommendations to see insights here.
                </p>
              </div>
            )}
          </Card>

          <Card>
            <h3 className="mb-3 font-semibold">🕒 Recent Runs</h3>

            {recentRuns.length > 0 ? (
              <div className="space-y-2">
                {recentRuns.map((run) => (
                  <div
                    key={run.id}
                    className="flex justify-between rounded border p-3 transition hover:scale-[1.01] hover:shadow-sm dark:border-gray-700"
                  >
                    <span>{run.project_type}</span>
                    <span className="text-sm text-gray-500 dark:text-gray-300">
                      {getLanguageDisplay(run.winner_language)}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="py-10 text-center text-gray-500 dark:text-gray-300">
                <p className="text-lg">No runs yet</p>
                <p className="text-sm">
                  Generate recommendations to populate this section.
                </p>
              </div>
            )}
          </Card>
        </>
      )}
    </motion.div>
  );
}