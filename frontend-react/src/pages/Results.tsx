import { useLocation } from "react-router-dom";
import RecommendationCard from "../components/RecommendationCard";
import ConfidenceBar from "../components/ConfidenceBar";
import SensitivityTable from "../components/SensitivityTable";
import ParetoChart from "../components/ParetoChart";
import WhyNotList from "../components/WhyNotList";
import type { RecommendationResponse } from "../types/api";

export default function Results() {
  const location = useLocation();
  const data = location.state as RecommendationResponse | undefined;

  if (!data) {
    return (
      <div className="rounded-xl border bg-white p-6 shadow-sm">
        <h1 className="text-2xl font-bold">Results</h1>
        <p className="mt-2 text-gray-600">No result loaded.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Results</h1>
        <p className="mt-2 text-gray-600">
          Review the recommended stack, confidence, trade-offs, and alternatives.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
        <RecommendationCard winner={data.winner} />
        <ConfidenceBar value={data.confidence} />
      </div>

      <SensitivityTable sensitivity={data.sensitivity} />

      <ParetoChart data={data.pareto ?? []} />

      <WhyNotList items={data.why_not} />
    </div>
  );
}