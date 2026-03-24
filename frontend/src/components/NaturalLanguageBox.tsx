import { useState } from "react";
import API from "../api/client";
import type { NaturalLanguageRecommendationResponse } from "../types/api";

type Props = {
  onResult: (result: NaturalLanguageRecommendationResponse) => void;
};

export default function NaturalLanguageBox({ onResult }: Props) {
  const [query, setQuery] = useState(
    "I want a scalable backend for an API with low ops and Python-friendly tooling"
  );
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit() {
    setLoading(true);
    setError(null);

    try {
      const res = await API.post<NaturalLanguageRecommendationResponse>(
        "/recommend/natural-language",
        { query }
      );
      onResult(res.data);
    } catch {
      setError("Could not process natural language query.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="rounded-2xl border bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
      <h2 className="text-lg font-semibold">🧠 Natural Language Input</h2>
      <p className="mt-2 text-sm text-gray-500 dark:text-gray-300">
        Describe your project in plain English and let StackWise AI convert it
        into structured recommendation inputs.
      </p>

      <textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        rows={4}
        className="mt-4 w-full rounded-xl border p-3 dark:border-gray-700 dark:bg-gray-900"
        placeholder="Example: I want a scalable backend for real-time apps with low ops"
      />

      {error && (
        <div className="mt-3 rounded-xl bg-red-100 p-3 text-red-700 dark:bg-red-900/30 dark:text-red-300">
          {error}
        </div>
      )}

      <button
        onClick={handleSubmit}
        disabled={loading || !query.trim()}
        className="mt-4 rounded-xl bg-linear-to-r from-fuchsia-600 to-violet-600 px-5 py-3 text-white shadow transition hover:scale-[1.02] hover:shadow-lg disabled:opacity-60"
      >
        {loading ? "Analyzing..." : "Generate from Text"}
      </button>
    </div>
  );
}