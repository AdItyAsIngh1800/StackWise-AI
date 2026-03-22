import { useEffect, useState } from "react";
import { NavLink } from "react-router-dom";

type Props = {
  children: React.ReactNode;
};

export default function Layout({ children }: Props) {
  // ✅ Initialize state directly (no useEffect needed)
  const [darkMode, setDarkMode] = useState<boolean>(() => {
    return localStorage.getItem("darkMode") === "true";
  });

  // ✅ Sync DOM + localStorage
  useEffect(() => {
    const root = document.documentElement;

    if (darkMode) {
      root.classList.add("dark");
    } else {
      root.classList.remove("dark");
    }

    localStorage.setItem("darkMode", String(darkMode));
  }, [darkMode]);

  const navClass = ({ isActive }: { isActive: boolean }) =>
    `rounded-lg px-3 py-2 text-sm font-medium transition ${
      isActive
        ? "bg-blue-600 text-white"
        : "text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800"
    }`;

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 dark:bg-gray-900 dark:text-white">
      <header className="border-b bg-white shadow-sm dark:border-gray-700 dark:bg-gray-800">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div>
            <h1 className="text-xl font-bold">🚀 StackWise-AI</h1>
            <p className="text-sm text-gray-500 dark:text-gray-300">
              Explainable tech stack decision support system
            </p>
          </div>

          <div className="flex items-center gap-4">
            <nav className="flex gap-2">
              <NavLink to="/" className={navClass}>
                Home
              </NavLink>
              <NavLink to="/results" className={navClass}>
                Results
              </NavLink>
              <NavLink to="/analytics" className={navClass}>
                Analytics
              </NavLink>
            </nav>

            <button
              onClick={() => setDarkMode((prev) => !prev)}
              className="rounded-lg border px-3 py-2 text-sm transition hover:bg-gray-100 dark:border-gray-600 dark:hover:bg-gray-700"
            >
              {darkMode ? "☀️ Light" : "🌙 Dark"}
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl p-6">{children}</main>

      <footer className="border-t py-4 text-center text-sm text-gray-500 dark:border-gray-700 dark:text-gray-400">
        <p>StackWise AI • Decision Support System for Tech Stack Selection</p>
      </footer>
    </div>
  );
}