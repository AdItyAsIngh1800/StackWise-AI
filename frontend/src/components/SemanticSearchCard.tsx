import { useState } from "react";
import API from "../api/client";
import type { SemanticSearchResult } from "../types/api";

export default function SemanticSearchCard() {
  const [query, setQuery] = useState("fast backend for scalable systems");
  const [results, setResults] = useState<SemanticSearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSearch() {
    if (!query.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const res = await API.get<SemanticSearchResult[]>("/semantic-search", {
        params: { query, top_k: 4 },
      });
      setResults(res.data);
    } catch {
      setError("Semantic search failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="rounded-2xl border bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
      <h2 className="text-lg font-semibold">🔎 Semantic Search</h2>
      <p className="mt-2 text-sm text-gray-500 dark:text-gray-300">
        Search languages by meaning using embedding similarity.
      </p>

      <div className="mt-4 flex gap-3">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g. fast backend for scalable systems"
          className="flex-1 rounded-xl border p-3 dark:border-gray-700 dark:bg-gray-900"
        />
        <button
          onClick={handleSearch}
          disabled={loading}
          className="rounded-xl bg-linear-to-r from-fuchsia-600 to-violet-600 px-4 py-2 text-white shadow hover:scale-[1.02] disabled:opacity-60"
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </div>

      {error && (
        <div className="mt-4 rounded-xl bg-red-100 p-3 text-red-700 dark:bg-red-900/30 dark:text-red-300">
          {error}
        </div>
      )}

      {results.length > 0 && (
        <div className="mt-4 space-y-3">
          {results.map((item) => (
            <div
              key={item.language}
              className="flex items-center justify-between rounded-xl border p-4 dark:border-gray-700"
            >
              <span className="font-medium">{item.language}</span>
              <span className="rounded-full bg-violet-100 px-3 py-1 text-sm text-violet-700 dark:bg-violet-900/30 dark:text-violet-300">
                similarity {item.similarity.toFixed(4)}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}