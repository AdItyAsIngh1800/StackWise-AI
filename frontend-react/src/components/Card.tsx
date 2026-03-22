type Props = {
  children: React.ReactNode;
};

export default function Card({ children }: Props) {
  return (
    <div className="bg-white p-4 rounded-xl shadow hover:shadow-md transition">
      {children}
    </div>
  );
}