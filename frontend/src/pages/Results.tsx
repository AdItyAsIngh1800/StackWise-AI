import { useLocation, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

import RecommendationCard from "../components/RecommendationCard";
import ConfidenceBar from "../components/ConfidenceBar";
import SensitivityTable from "../components/SensitivityTable";
import ParetoChart from "../components/ParetoChart";
import WhyNotList from "../components/WhyNotList";
import RankingChart from "../components/RankingChart";
import SimilarStacksCard from "../components/SimilarStacksCard";
import type { RecommendationResponse } from "../types/api";
import Card from "../components/Card";

export default function Results() {
  const location = useLocation();
  const navigate = useNavigate();
  const data = location.state as RecommendationResponse | undefined;

  if (!data) {
    return (
      <motion.div className="py-20 text-center">
        <h2 className="text-xl font-semibold">No Results Found</h2>
        <p className="mt-2 text-gray-500 dark:text-gray-300">
          Go back and generate a recommendation first.
        </p>
        <button
          onClick={() => navigate("/")}
          className="mt-6 rounded-xl bg-blue-600 px-5 py-2 text-white transition hover:bg-blue-700"
        >
          Go to Home
        </button>
      </motion.div>
    );
  }

  const winner = data.winner;

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-8"
    >
      <section className="rounded-3xl bg-linear-to-r from-blue-600 via-violet-600 to-fuchsia-600 p-8 text-white shadow-lg">
        <h1 className="text-3xl font-bold">Recommendation Results</h1>
        <p className="mt-2 text-white/90">
          Detailed explanation of your optimal tech stack decision.
        </p>
      </section>

      <Card>
        <h2 className="mb-2 text-lg font-semibold">📌 Summary</h2>
        <p className="text-gray-600 dark:text-gray-300">
          For your project, <b>{winner?.language}</b> with{" "}
          <b>{winner?.backend_framework}</b> is recommended due to strong
          ecosystem support, compatibility with your constraints, and balanced
          trade-offs.
        </p>
      </Card>

      <div className="rounded-2xl bg-linear-to-r from-green-500 to-emerald-500 p-5 text-white shadow transition hover:scale-[1.01] hover:shadow-lg">
        <h2 className="text-lg font-semibold">🏆 Best Choice</h2>
        <p className="mt-2 text-xl font-bold">
          {winner?.language} + {winner?.backend_framework}
        </p>
        <p className="text-sm opacity-90">
          Database: {winner?.database} | Deployment: {winner?.deployment}
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
        <RecommendationCard winner={winner} />
        <ConfidenceBar value={data.confidence ?? 0} />
      </div>

      <RankingChart data={data.ranked_languages ?? []} />

      <ParetoChart data={data.pareto ?? []} />

      <SimilarStacksCard items={data.similar_stacks} />

      <div className="border-t dark:border-gray-700" />

      <Card>
        <h3 className="mb-3 text-lg font-semibold">🔍 Sensitivity Analysis</h3>
        <SensitivityTable sensitivity={data.sensitivity} />
      </Card>

      <Card>
        <h3 className="mb-3 text-lg font-semibold">❌ Why Not Others</h3>
        <WhyNotList items={data.why_not} />
      </Card>

      <div className="flex justify-center">
        <button
          onClick={() => navigate("/")}
          className="rounded-xl bg-linear-to-r from-blue-600 to-violet-600 px-6 py-3 text-white shadow transition hover:scale-[1.02] hover:shadow-lg"
        >
          Run Another Scenario
        </button>
      </div>
    </motion.div>
  );
}