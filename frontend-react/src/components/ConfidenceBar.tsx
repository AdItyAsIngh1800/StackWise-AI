import { motion } from "framer-motion";

type Props = {
  value: number;
};

export default function ConfidenceBar({ value }: Props) {
  const percent = Math.max(0, Math.min(100, value * 100));

  return (
    <div className="rounded-2xl border bg-white p-5 shadow-sm dark:border-gray-700 dark:bg-gray-800">
      <h3 className="mb-3 text-lg font-semibold">🧠 Confidence Score</h3>

      <p className="mb-2 text-sm text-gray-500 dark:text-gray-300">
        Measures how stable the recommendation is.
      </p>

      <div className="mb-2 flex items-center justify-between">
        <span className="text-sm text-gray-500">0</span>
        <span className="text-sm text-gray-500">1</span>
      </div>

      <div className="h-4 w-full rounded-full bg-gray-200 dark:bg-gray-700 overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percent}%` }}
          transition={{ duration: 0.6 }}
          className="h-4 rounded-full bg-linear-to-r from-blue-500 via-violet-500 to-fuchsia-500"
        />
      </div>

      <p className="mt-3 text-right text-sm font-medium">
        {value.toFixed(3)}
      </p>
    </div>
  );
}