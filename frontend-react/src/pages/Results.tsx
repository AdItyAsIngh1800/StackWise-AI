import { useLocation } from "react-router-dom";
import RecommendationCard from "../components/RecommendationCard";
import ConfidenceBar from "../components/ConfidenceBar";
import SensitivityTable from "../components/SensitivityTable";
import ParetoChart from "../components/ParetoChart";
import WhyNotList from "../components/WhyNotList";
import RankingChart from "../components/RankingChart";
import type { RecommendationResponse } from "../types/api";
import Card from "../components/Card";

export default function Results() {
  const location = useLocation();
  const data = location.state as RecommendationResponse | undefined;

  if (!data) {
    return (
      <Card>
        <h1 className="text-2xl font-bold">Results</h1>
        <p className="mt-2 text-gray-600 dark:text-gray-300">
          No result loaded. Go back to Home and generate a recommendation first.
        </p>
      </Card>
    );
  }

  const winner = data.winner;
  const summary = winner
    ? `Recommended stack: ${winner.language} + ${winner.backend_framework ?? "-"} + ${winner.database ?? "-"} + ${winner.deployment ?? "-"}.`
    : "No recommendation available.";

  return (
    <div className="space-y-6">
      <section className="rounded-2xl bg-white p-6 shadow-sm dark:bg-gray-800">
        <h1 className="text-3xl font-bold">Results</h1>
        <p className="mt-2 text-gray-600 dark:text-gray-300">
          Review the recommendation, confidence level, ranking, trade-offs, and
          reasons behind the decision.
        </p>
      </section>

      <Card>
        <h2 className="mb-2 text-lg font-semibold">📌 Final Decision</h2>
        <p className="text-gray-700 dark:text-gray-200">{summary}</p>
      </Card>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
        <RecommendationCard winner={data.winner} />
        <ConfidenceBar value={data.confidence} />
      </div>

      <RankingChart data={data.ranked_languages ?? []} />

      <SensitivityTable sensitivity={data.sensitivity} />

      <ParetoChart data={data.pareto ?? []} />

      <WhyNotList items={data.why_not} />
    </div>
  );
}