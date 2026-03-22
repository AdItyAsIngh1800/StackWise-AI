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
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="text-center py-20"
      >
        <h2 className="text-xl font-semibold">No Results Found</h2>
        <p className="mt-2 text-gray-500">
          Generate a recommendation first.
        </p>
      </motion.div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="space-y-6"
    >
      <section className="rounded-2xl bg-white p-6 shadow-sm dark:bg-gray-800">
        <h1 className="text-3xl font-bold">Results</h1>
      </section>

      <Card>
        <h2 className="mb-2 font-semibold">📌 Final Decision</h2>
        <p>{data.winner?.language}</p>
      </Card>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
        <RecommendationCard winner={data.winner} />
        <ConfidenceBar value={data.confidence} />
      </div>

      <RankingChart data={data.ranked_languages ?? []} />

      <SensitivityTable sensitivity={data.sensitivity} />

      <ParetoChart data={data.pareto ?? []} />

      <WhyNotList items={data.why_not} />
    </motion.div>
  );
}