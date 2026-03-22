type Props = {
  children: React.ReactNode;
};

export default function Layout({ children }: Props) {
  return (
    <div className="min-h-screen bg-gray-50">
      
      {/* Navbar */}
      <div className="bg-white shadow px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold">🚀 StackWise-AI</h1>
        <div className="flex gap-6 text-sm">
          <a href="/" className="hover:text-blue-600">Home</a>
          <a href="/analytics" className="hover:text-blue-600">Analytics</a>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-6xl mx-auto p-6">
        {children}
      </div>

    </div>
  );
}