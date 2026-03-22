type Props = {
  items?: { language: string; reason: string }[] | null;
};

export default function WhyNotList({ items }: Props) {
  return (
    <div className="rounded-xl border p-4 shadow-sm">
      <h3 className="mb-3 text-lg font-semibold">❌ Why Not Selected</h3>
      {!items || items.length === 0 ? (
        <p>No comparison insights available.</p>
      ) : (
        <ul className="space-y-2">
          {items.map((item) => (
            <li key={item.language}>
              <strong>{item.language}</strong>: {item.reason}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}