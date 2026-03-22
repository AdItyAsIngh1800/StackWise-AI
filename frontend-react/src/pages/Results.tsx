import { useLocation } from "react-router-dom";
import { motion } from "framer-motion";

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
      <motion.div className="py-20 text-center">
        <h2 className="text-xl font-semibold">No Results Found</h2>
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

      <div className="rounded-2xl bg-linear-to-r from-green-500 to-emerald-500 p-5 text-white shadow">
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

      <Card>
        <h3 className="mb-3 font-semibold">🔍 Sensitivity Analysis</h3>
        <SensitivityTable sensitivity={data.sensitivity} />
      </Card>

      <Card>
        <h3 className="mb-3 font-semibold">❌ Why Not Others</h3>
        <WhyNotList items={data.why_not} />
      </Card>
    </motion.div>
  );
}