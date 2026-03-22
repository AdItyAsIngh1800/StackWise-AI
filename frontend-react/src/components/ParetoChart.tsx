import { ResponsiveContainer, ScatterChart, Scatter, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

type Props = {
  data: { language: string; score: number; ecosystem: number }[];
};

export default function ParetoChart({ data }: Props) {
  return (
    <div className="rounded-xl border p-4 shadow-sm">
      <h3 className="mb-3 text-lg font-semibold">⚖️ Pareto Frontier</h3>
      <div style={{ width: "100%", height: 320 }}>
        <ResponsiveContainer>
          <ScatterChart>
            <CartesianGrid />
            <XAxis type="number" dataKey="ecosystem" name="ecosystem" />
            <YAxis type="number" dataKey="score" name="score" />
            <Tooltip cursor={{ strokeDasharray: "3 3" }} />
            <Scatter data={data} />
          </ScatterChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}