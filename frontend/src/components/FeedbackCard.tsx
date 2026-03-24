import { useState } from "react";
import API from "../api/client";
import type {
  FeedbackRequest,
  FeedbackResponse,
  RecommendationContext,
  StackRecommendation,
} from "../types/api";

type Props = {
  winner: StackRecommendation | null;
  alternatives: StackRecommendation[];
  context: RecommendationContext;
  runId?: number | null;
};

export default function FeedbackCard({
  winner,
  alternatives,
  context,
  runId = null,
}: Props) {
  const [selectedLanguage, setSelectedLanguage] = useState<string>(
    winner?.language ?? ""
  );
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [accepted, setAccepted] = useState<boolean | null>(null);
  const [error, setError] = useState<string | null>(null);

  if (!winner) return null;

  const safeWinner = winner;

  async function submitFeedback(language: string) {
    setLoading(true);
    setError(null);

    const payload: FeedbackRequest = {
      run_id: runId,
      ...context,
      recommended_language: safeWinner.language,
      selected_language: language,
    };

    try {
      const res = await API.post<FeedbackResponse>("/feedback", payload);
      setAccepted(res.data.accepted);
      setSubmitted(true);
    } catch {
      setError("Could not submit feedback.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="rounded-2xl border bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
      <h3 className="text-lg font-semibold">📝 Feedback</h3>
      <p className="mt-2 text-sm text-gray-500 dark:text-gray-300">
        Help improve future recommendations by confirming or correcting this result.
      </p>

      {submitted ? (
        <div className="mt-4 rounded-xl bg-emerald-100 p-4 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300">
          {accepted
            ? "Thanks — you accepted the recommendation."
            : `Thanks — feedback saved. You preferred ${selectedLanguage}.`}
        </div>
      ) : (
        <>
          <div className="mt-4 flex flex-wrap gap-3">
            <button
              onClick={() => submitFeedback(safeWinner.language)}
              disabled={loading}
              className="rounded-xl bg-emerald-600 px-4 py-2 text-white transition hover:bg-emerald-700 disabled:opacity-60"
            >
              👍 Yes, this is good
            </button>

            <button
              onClick={() => setSelectedLanguage("")}
              disabled={loading}
              className="rounded-xl bg-amber-500 px-4 py-2 text-white transition hover:bg-amber-600 disabled:opacity-60"
            >
              👎 I prefer another option
            </button>
          </div>

          <div className="mt-4">
            <label className="mb-2 block text-sm font-medium">
              If not, which language would you choose?
            </label>

            <select
              value={selectedLanguage}
              onChange={(e) => setSelectedLanguage(e.target.value)}
              className="w-full rounded-xl border p-3 dark:border-gray-700 dark:bg-gray-900"
            >
              <option value="">Select an alternative</option>
              <option value={safeWinner.language}>{safeWinner.language}</option>
              {alternatives.map((alt) => (
                <option key={alt.language} value={alt.language}>
                  {alt.language}
                </option>
              ))}
            </select>

            <button
              onClick={() => selectedLanguage && submitFeedback(selectedLanguage)}
              disabled={loading || !selectedLanguage}
              className="mt-3 rounded-xl bg-linear-to-r from-blue-600 to-violet-600 px-4 py-2 text-white shadow transition hover:scale-[1.02] disabled:opacity-60"
            >
              {loading ? "Submitting..." : "Submit Alternative Choice"}
            </button>
          </div>

          {error && (
            <div className="mt-4 rounded-xl bg-red-100 p-3 text-red-700 dark:bg-red-900/30 dark:text-red-300">
              {error}
            </div>
          )}
        </>
      )}
    </div>
  );
}