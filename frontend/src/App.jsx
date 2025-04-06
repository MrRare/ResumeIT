import React, { useState } from "react";
import axios from "axios";

function App() {
  const [jdText, setJdText] = useState("");
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (!jdText.trim()) {
      setError("Please enter a job description");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await axios.post("http://localhost:5000/match", {
        jd_text: jdText,
      });
      setMatches(response.data.matches);
    } catch (err) {
      console.error("Error fetching matches:", err);
      setError(err.response?.data?.error || "Failed to connect to the server");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-2xl bg-white p-6 rounded shadow text-center">
        <h1 className="text-2xl font-bold mb-4">Resume Job Matcher</h1>
        <p className="mb-4">Paste a job description to find matching resumes in your database.</p>

        <div className="mb-4">
          <textarea
            value={jdText}
            onChange={(e) => setJdText(e.target.value)}
            rows="10"
            className="w-full p-2 border border-gray-300 rounded"
            placeholder="Paste job description here..."
          />
        </div>

        <button
          onClick={handleSubmit}
          disabled={loading}
          className="bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded"
        >
          {loading ? "Finding Matches..." : "Find Matching Resumes"}
        </button>

        {error && (
          <div className="mt-4 p-2 bg-red-100 text-red-700 rounded">
            {error}
          </div>
        )}

        {matches.length > 0 && (
          <div className="mt-6 text-left">
            <h2 className="text-xl font-semibold mb-3">Top Matching Resumes:</h2>
            <ul className="bg-gray-50 p-4 rounded">
              {matches.map((file, idx) => (
                <li key={idx} className="py-2 border-b last:border-0">
                  <span className="font-medium">{idx + 1}.</span> {file}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
