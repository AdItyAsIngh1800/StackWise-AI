import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Cell,
} from "recharts";

type Props = {
  data: { language: string; score: number }[];
};

const BAR_COLORS = [
  "#2563eb", // blue
  "#7c3aed", // violet
  "#db2777", // pink
  "#10b981", // emerald
  "#f59e0b", // amber
  "#ef4444", // red
];

export default function RankingChart({ data }: Props) {
  return (
    <div className="rounded-2xl border bg-white p-5 shadow-sm dark:border-gray-700 dark:bg-gray-800">
      <h3 className="mb-3 text-lg font-semibold">📊 Language Ranking</h3>
      <p className="mb-4 text-sm text-gray-500 dark:text-gray-300">
        Higher score means better overall fit for the current project profile.
      </p>

      <div style={{ width: "100%", height: 320 }}>
        <ResponsiveContainer>
          <BarChart
            data={data}
            margin={{ top: 10, right: 20, left: 0, bottom: 10 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#cbd5e1" />
            <XAxis dataKey="language" stroke="#64748b" />
            <YAxis domain={[0, 1]} stroke="#64748b" />
            <Tooltip
              contentStyle={{
                backgroundColor: "#111827",
                border: "none",
                borderRadius: "12px",
                color: "#ffffff",
              }}
              formatter={(value) => [
                typeof value === "number" ? value.toFixed(3) : String(value ?? ""),
                "Score",
              ]}
            />
            <Bar dataKey="score" radius={[8, 8, 0, 0]}>
              {data.map((entry, index) => (
                <Cell
                  key={`cell-${entry.language}`}
                  fill={BAR_COLORS[index % BAR_COLORS.length]}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}