import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import api from "../api/apiClient";

const JobHistoryDetailsPage = () => {
  const { historyId } = useParams();
  const [history, setHistory] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const fetchHistoryDetails = async () => {
    setLoading(true);
    try {
      const res = await api.get(`/history/${historyId}/`);
      setHistory(res.data);
    } catch (err) {
      console.error(err);
      alert("Failed to load history details");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistoryDetails();
  }, [historyId]);

  const handleDownloadReport = () => {
    window.open(
      `${process.env.REACT_APP_API_BASE_URL}/history/${historyId}/download/`,
      '_blank'
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <div className="text-6xl mb-4">⏳</div>
            <p className="text-xl text-gray-600">Loading details...</p>
          </div>
        </div>
      </div>
    );
  }

  if (!history) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="max-w-4xl mx-auto px-4 py-20 text-center">
          <div className="text-6xl mb-4">❌</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-4">History Not Found</h2>
          <button
            onClick={() => navigate("/history")}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700"
          >
            Back to History
          </button>
        </div>
      </div>
    );
  }

  const results = history.results_data || [];

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-md p-8 mb-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">{history.job_title}</h1>
              <p className="text-sm text-gray-500">
                Screened on {new Date(history.created_at).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit'
                })}
              </p>
            </div>
            <div className="flex gap-3">
              <button
                onClick={handleDownloadReport}
                className="bg-green-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-green-700 transition-colors flex items-center space-x-2"
              >
                <span>📥</span>
                <span>Download PDF Report</span>
              </button>
              <button
                onClick={() => navigate("/history")}
                className="bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
              >
                Back to History
              </button>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
              <div className="text-sm text-gray-600 mb-1">Total Candidates</div>
              <div className="text-2xl font-bold text-blue-600">{history.total_resumes}</div>
            </div>
            <div className="bg-green-50 rounded-lg p-4 border border-green-200">
              <div className="text-sm text-gray-600 mb-1">Top Candidate</div>
              <div className="text-lg font-semibold text-green-600 truncate">
                {history.top_candidate || "N/A"}
              </div>
            </div>
            <div className="bg-purple-50 rounded-lg p-4 border border-purple-200">
              <div className="text-sm text-gray-600 mb-1">Highest Score</div>
              <div className="text-2xl font-bold text-purple-600">
                {history.highest_score?.toFixed(2) || "N/A"}
              </div>
            </div>
          </div>
        </div>

        {/* Job Description */}
        <div className="bg-white rounded-lg shadow-md p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Job Description</h2>
          <p className="text-gray-700 whitespace-pre-wrap">{history.job_description}</p>
        </div>

        {/* Results */}
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="bg-gradient-to-r from-blue-600 to-blue-700 px-6 py-4">
            <h2 className="text-2xl font-bold text-white">Candidate Rankings</h2>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-100">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Rank</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Candidate</th>
                  <th className="px-6 py-4 text-center text-sm font-semibold text-gray-700">Final Score</th>
                  <th className="px-6 py-4 text-center text-sm font-semibold text-gray-700">Keyword</th>
                  <th className="px-6 py-4 text-center text-sm font-semibold text-gray-700">Semantic</th>
                  <th className="px-6 py-4 text-center text-sm font-semibold text-gray-700">LLM Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {results.map((r, i) => (
                  <tr key={i} className={`hover:bg-gray-50 ${i < 3 ? "bg-blue-50" : ""}`}>
                    <td className="px-6 py-4">
                      <div className={`inline-flex items-center justify-center w-10 h-10 rounded-full font-bold ${
                        i === 0 ? "bg-yellow-400 text-yellow-900" :
                        i === 1 ? "bg-gray-300 text-gray-800" :
                        i === 2 ? "bg-orange-400 text-orange-900" :
                        "bg-blue-100 text-blue-800"
                      }`}>
                        {i + 1}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="font-semibold text-gray-900">{r.filename}</div>
                    </td>
                    <td className="px-6 py-4 text-center">
                      <div className={`text-2xl font-bold ${
                        r.final_score >= 70 ? "text-green-600" :
                        r.final_score >= 50 ? "text-yellow-600" :
                        "text-red-600"
                      }`}>
                        {r.final_score.toFixed(2)}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-center text-gray-600">
                      {r.keyword_score.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 text-center text-gray-600">
                      {r.semantic_score.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 text-center">
                      {r.llm_analyzed ? (
                        <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          ✓ Analyzed
                        </span>
                      ) : (
                        <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700">
                          ⚡ Skipped
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobHistoryDetailsPage;
