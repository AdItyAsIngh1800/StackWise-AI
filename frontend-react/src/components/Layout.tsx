import { Link } from "react-router-dom";

type Props = {
  children: React.ReactNode;
};

function getInitialDarkMode(): boolean {
  if (typeof window === "undefined") return false;
  return localStorage.getItem("darkMode") === "true";
}

export default function Layout({ children }: Props) {
  const darkMode = getInitialDarkMode();

  if (darkMode) {
    document.documentElement.classList.add("dark");
  } else {
    document.documentElement.classList.remove("dark");
  }

  function toggleDarkMode() {
    const next = !darkMode;

    if (next) {
      document.documentElement.classList.add("dark");
      localStorage.setItem("darkMode", "true");
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("darkMode", "false");
    }

    window.location.reload();
  }

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 dark:bg-gray-900 dark:text-gray-100">
      <header className="border-b bg-white shadow-sm dark:border-gray-700 dark:bg-gray-800">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div>
            <h1 className="text-xl font-bold">🚀 StackWise-AI</h1>
            <p className="text-sm text-gray-500 dark:text-gray-300">
              Explainable tech stack decision support system
            </p>
          </div>

          <div className="flex items-center gap-6">
            <nav className="flex gap-4 text-sm font-medium">
              <Link to="/" className="hover:text-blue-600">
                Home
              </Link>
              <Link to="/analytics" className="hover:text-blue-600">
                Analytics
              </Link>
            </nav>

            <button
              onClick={toggleDarkMode}
              className="rounded-lg border px-3 py-1 text-sm transition hover:bg-gray-100 dark:border-gray-600 dark:hover:bg-gray-700"
            >
              {darkMode ? "☀️ Light" : "🌙 Dark"}
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl p-6">{children}</main>
    </div>
  );
}