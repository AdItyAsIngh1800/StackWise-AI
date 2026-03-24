type ParsedInput = {
  project_type: string;
  team_languages: string[];
  low_ops: boolean;
  expected_scale: string;
  prefer_enterprise: boolean;
  prototype_only: boolean;
  rapid_schema_changes: boolean;
  needs_cache: boolean;
  prefer_portability: boolean;
};

type Props = {
  parsed: ParsedInput;
};

function Badge({
  label,
  active,
}: {
  label: string;
  active: boolean;
}) {
  return (
    <span
      className={`rounded-full px-3 py-1 text-sm ${
        active
          ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300"
          : "bg-gray-100 text-gray-500 dark:bg-gray-700 dark:text-gray-300"
      }`}
    >
      {label}
    </span>
  );
}

export default function ParsedInputCard({ parsed }: Props) {
  return (
    <div className="rounded-2xl border bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
      <h2 className="text-lg font-semibold">🧾 Parsed Inputs</h2>
      <p className="mt-2 text-sm text-gray-500 dark:text-gray-300">
        This is how the natural-language query was interpreted by the system.
      </p>

      <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2">
        <div>
          <p className="text-sm text-gray-500 dark:text-gray-300">Project Type</p>
          <p className="font-medium">{parsed.project_type}</p>
        </div>

        <div>
          <p className="text-sm text-gray-500 dark:text-gray-300">Expected Scale</p>
          <p className="font-medium">{parsed.expected_scale}</p>
        </div>

        <div className="md:col-span-2">
          <p className="text-sm text-gray-500 dark:text-gray-300">Team Languages</p>
          <div className="mt-2 flex flex-wrap gap-2">
            {parsed.team_languages.length > 0 ? (
              parsed.team_languages.map((lang) => (
                <span
                  key={lang}
                  className="rounded-full bg-blue-100 px-3 py-1 text-sm text-blue-700 dark:bg-blue-900/30 dark:text-blue-300"
                >
                  {lang}
                </span>
              ))
            ) : (
              <span className="text-sm text-gray-500 dark:text-gray-300">
                None inferred
              </span>
            )}
          </div>
        </div>

        <div className="md:col-span-2 flex flex-wrap gap-2">
          <Badge label="Low Ops" active={parsed.low_ops} />
          <Badge label="Enterprise" active={parsed.prefer_enterprise} />
          <Badge label="Prototype" active={parsed.prototype_only} />
          <Badge label="Rapid Schema" active={parsed.rapid_schema_changes} />
          <Badge label="Needs Cache" active={parsed.needs_cache} />
          <Badge label="Portability" active={parsed.prefer_portability} />
        </div>
      </div>
    </div>
  );
}
