import Card from "./Card";
import type { StackRecommendation } from "../types/api";

type Props = {
  winner: StackRecommendation | null;
};

export default function RecommendationCard({ winner }: Props) {
  if (!winner) return <Card>No recommendation available</Card>;

  return (
    <Card>
      <h2 className="text-lg font-semibold mb-3">🏆 Recommended Stack</h2>

      <div className="space-y-1 text-sm">
        <p><b>Language:</b> {winner.language}</p>
        <p><b>Framework:</b> {winner.backend_framework ?? "-"}</p>
        <p><b>Database:</b> {winner.database ?? "-"}</p>
        <p><b>Deployment:</b> {winner.deployment ?? "-"}</p>
      </div>

      <div className="mt-3 text-blue-600 font-semibold">
        Score: {winner.score.toFixed(3)}
      </div>
    </Card>
  );
}