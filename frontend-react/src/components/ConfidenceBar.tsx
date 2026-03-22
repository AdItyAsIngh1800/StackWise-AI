type Props = {
  value?: number | null;
};

export default function ConfidenceBar({ value }: Props) {
  const safeValue = value ?? 0; // 👈 handle null/undefined
  const pct = Math.max(0, Math.min(100, safeValue * 100));

  return (
    <div className="rounded-xl border p-4 shadow-sm">
      <h3 className="mb-2 text-lg font-semibold">📈 Confidence</h3>
      <div className="mb-2 text-sm">{safeValue.toFixed(3)}</div>
      <div className="h-3 w-full rounded bg-gray-200">
        <div
          className="h-3 rounded bg-blue-600"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}