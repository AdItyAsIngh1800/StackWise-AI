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

  if (!data) return <div>No result loaded.</div>;

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Results</h1>
      <RecommendationCard winner={data.winner} />
      <ConfidenceBar value={data.confidence} />
      <SensitivityTable sensitivity={data.sensitivity} />
      <ParetoChart data={data.pareto ?? []} />
      <WhyNotList items={data.why_not} />
    </div>
  );
}