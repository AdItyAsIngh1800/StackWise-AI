import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

type Props = {
  data: { language: string; score: number }[];
};

export default function RankingChart({ data }: Props) {
  return (
    <div className="rounded-xl border bg-white p-4 shadow-sm dark:border-gray-700 dark:bg-gray-800">
      <h3 className="mb-3 text-lg font-semibold">📊 Language Ranking</h3>

      <div style={{ width: "100%", height: 320 }}>
        <ResponsiveContainer>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="language" />
            <YAxis domain={[0, 1]} />
            <Tooltip
              formatter={(value) => [
                typeof value === "number" ? value.toFixed(3) : String(value ?? ""),
                "Score",
              ]}
            />
            <Bar dataKey="score" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}