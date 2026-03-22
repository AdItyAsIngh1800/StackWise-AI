export default function LoadingSpinner() {
  return (
    <div className="flex items-center gap-3 rounded-xl border bg-white p-4 shadow-sm dark:border-gray-700 dark:bg-gray-800">
      <div className="h-5 w-5 animate-spin rounded-full border-2 border-blue-600 border-t-transparent" />
      <span className="text-sm text-gray-700 dark:text-gray-200">
        Generating recommendation...
      </span>
    </div>
  );
}