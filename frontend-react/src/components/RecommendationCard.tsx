import type { StackRecommendation } from "../types/api";

type Props = {
  winner: StackRecommendation | null;
};

export default function RecommendationCard({ winner }: Props) {
  if (!winner) {
    return <div className="rounded-xl border p-4">No recommendation available.</div>;
  }

  return (
    <div className="rounded-xl border p-4 shadow-sm">
      <h2 className="mb-3 text-xl font-semibold">🏆 Recommended Stack</h2>
      <p><strong>Language:</strong> {winner.language}</p>
      <p><strong>Framework:</strong> {winner.backend_framework ?? "-"}</p>
      <p><strong>Database:</strong> {winner.database ?? "-"}</p>
      <p><strong>Deployment:</strong> {winner.deployment ?? "-"}</p>
      <p><strong>Score:</strong> {winner.score.toFixed(3)}</p>
    </div>
  );
}