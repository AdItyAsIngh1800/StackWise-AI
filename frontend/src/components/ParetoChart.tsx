import {
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ZAxis,
  Cell,
} from "recharts";

type Props = {
  data: { language: string; score: number; ecosystem: number }[];
};

const DOT_COLORS = [
  "#2563eb",
  "#7c3aed",
  "#db2777",
  "#10b981",
  "#f59e0b",
  "#ef4444",
];

export default function ParetoChart({ data }: Props) {
  const chartData = data.map((item, index) => ({
    ...item,
    size: 120 + index * 20,
  }));

  return (
    <div className="rounded-2xl border bg-white p-5 shadow-sm dark:border-gray-700 dark:bg-gray-800">
      <h3 className="mb-3 text-lg font-semibold">⚖️ Pareto Trade-off</h3>

      <p className="mb-4 text-sm text-gray-500 dark:text-gray-300">
        Balance between ecosystem strength and recommendation score.
      </p>

      <div style={{ width: "100%", height: 340 }}>
        <ResponsiveContainer>
          <ScatterChart>
            <CartesianGrid stroke="#cbd5e1" />
            <XAxis
              type="number"
              dataKey="ecosystem"
              name="Ecosystem"
              domain={[0, 1]}
              stroke="#64748b"
            />
            <YAxis
              type="number"
              dataKey="score"
              name="Score"
              domain={[0, 1]}
              stroke="#64748b"
            />
            <ZAxis type="number" dataKey="size" range={[80, 280]} />

            <Tooltip
              contentStyle={{
                backgroundColor: "#111827",
                borderRadius: "12px",
                color: "#fff",
                border: "none",
              }}
              formatter={(value, name) => {
                const formatted =
                  typeof value === "number"
                    ? value.toFixed(3)
                    : Array.isArray(value)
                      ? value.join(", ")
                      : String(value ?? "");
                return [formatted, String(name)];
              }}
              labelFormatter={(_, payload) =>
                payload?.[0]?.payload?.language ?? ""
              }
            />

            <Scatter data={chartData}>
              {chartData.map((entry, index) => (
                <Cell
                  key={`cell-${entry.language}`}
                  fill={DOT_COLORS[index % DOT_COLORS.length]}
                />
              ))}
            </Scatter>
          </ScatterChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}