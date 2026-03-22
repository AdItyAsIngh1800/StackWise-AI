import { useState } from "react";

const LANGUAGE_OPTIONS = [
  "python",
  "javascript",
  "typescript",
  "java",
  "go",
  "c++",
  "rust",
  "c#",
  "php",
];

type Props = {
  value: string[];
  onChange: (value: string[]) => void;
};

export default function LanguageSelector({ value, onChange }: Props) {
  const [open, setOpen] = useState(false);

  function toggle(lang: string) {
    if (value.includes(lang)) {
      onChange(value.filter((l) => l !== lang));
    } else {
      onChange([...value, lang]);
    }
  }

  function remove(lang: string) {
    onChange(value.filter((l) => l !== lang));
  }

  return (
    <div className="relative">
      {/* Selected Chips */}
      <div
        onClick={() => setOpen((prev) => !prev)}
        className="flex min-h-[44px] flex-wrap items-center gap-2 rounded-xl border p-2 cursor-pointer dark:border-gray-700 dark:bg-gray-900"
      >
        {value.length === 0 && (
          <span className="text-gray-400 text-sm">Select languages...</span>
        )}

        {value.map((lang) => (
          <span
            key={lang}
            className="flex items-center gap-1 rounded-full bg-blue-100 px-3 py-1 text-sm text-blue-700 dark:bg-blue-900 dark:text-blue-200"
          >
            {lang}
            <button
              onClick={(e) => {
                e.stopPropagation();
                remove(lang);
              }}
              className="text-xs hover:text-red-500"
            >
              ✕
            </button>
          </span>
        ))}
      </div>

      {/* Dropdown */}
      {open && (
        <div className="absolute z-10 mt-2 w-full rounded-xl border bg-white shadow-lg dark:border-gray-700 dark:bg-gray-800">
          {LANGUAGE_OPTIONS.map((lang) => {
            const selected = value.includes(lang);

            return (
              <div
                key={lang}
                onClick={() => toggle(lang)}
                className={`cursor-pointer px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-700 ${
                  selected ? "bg-blue-50 dark:bg-blue-900/30" : ""
                }`}
              >
                {selected ? "✓ " : ""} {lang}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}