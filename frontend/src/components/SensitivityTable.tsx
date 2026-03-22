import type { RecommendationResponse } from "../types/api";

type Props = {
  sensitivity: RecommendationResponse["sensitivity"];
};

export default function SensitivityTable({ sensitivity }: Props) {
  if (!sensitivity) return <div className="rounded-xl border p-4">No sensitivity data.</div>;

  return (
    <div className="rounded-xl border p-4 shadow-sm">
      <h3 className="mb-3 text-lg font-semibold">🔍 Sensitivity Analysis</h3>
      <p><strong>Base winner:</strong> {sensitivity.base_winner ?? "-"}</p>
      <p><strong>Stability:</strong> {sensitivity.stability ?? "-"}</p>

      <table className="mt-3 w-full border-collapse text-sm">
        <thead>
          <tr>
            <th className="border p-2 text-left">Scenario</th>
            <th className="border p-2 text-left">Winner</th>
          </tr>
        </thead>
        <tbody>
          {(sensitivity.variations ?? []).map((row, idx) => (
            <tr key={idx}>
              <td className="border p-2">{row.scenario}</td>
              <td className="border p-2">{row.winner}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}