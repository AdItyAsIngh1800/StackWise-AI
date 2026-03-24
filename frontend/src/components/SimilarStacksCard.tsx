import type { SimilarStack } from "../types/api";

type Props = {
  items?: SimilarStack[] | null;
};

export default function SimilarStacksCard({ items }: Props) {
  return (
    <div className="rounded-2xl border bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
      <h3 className="text-lg font-semibold">🔁 Similar Stack Options</h3>
      <p className="mt-2 text-sm text-gray-500 dark:text-gray-300">
        Nearby alternatives based on ranking and ecosystem similarity.
      </p>

      {!items || items.length === 0 ? (
        <div className="mt-4 text-sm text-gray-500 dark:text-gray-300">
          No similar stack suggestions available.
        </div>
      ) : (
        <div className="mt-4 space-y-3">
          {items.map((item) => (
            <div
              key={item.language}
              className="flex items-center justify-between rounded-xl border p-4 dark:border-gray-700"
            >
              <div>
                <p className="font-medium capitalize">{item.language}</p>
                <p className="text-sm text-gray-500 dark:text-gray-300">
                  Score: {item.score.toFixed(3)}
                </p>
              </div>
              <div className="rounded-full bg-violet-100 px-3 py-1 text-sm text-violet-700 dark:bg-violet-900/30 dark:text-violet-300">
                distance {item.distance.toFixed(3)}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}