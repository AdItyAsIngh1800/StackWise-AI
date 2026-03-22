import { BrowserRouter, Link, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import Results from "./pages/Results";
import Analytics from "./pages/Analytics";

export default function App() {
  return (
    <BrowserRouter>
      <nav style={{ display: "flex", gap: 16, marginBottom: 24 }}>
        <Link to="/">Home</Link>
        <Link to="/analytics">Analytics</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/results" element={<Results />} />
        <Route path="/analytics" element={<Analytics />} />
      </Routes>
    </BrowserRouter>
  );
}