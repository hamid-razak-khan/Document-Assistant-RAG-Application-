import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import api from "../api/apiClient";

const JobHistoryPage = () => {
  const [history, setHistory] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const res = await api.get("/history/", { params: { search } });
      setHistory(res.data);
    } catch (err) {
      console.error(err);
      alert("Failed to load history");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, [search]);

  const handleSearch = (e) => {
    e.preventDefault();
    fetchHistory();
  };

  const handleClearHistory = async () => {
    if (window.confirm("Are you sure you want to clear all history? This action cannot be undone.")) {
      try {
        await api.delete("/history/clear/");
        fetchHistory(); // Refresh the history list
        alert("History cleared successfully");
      } catch (err) {
        console.error(err);
        alert("Failed to clear history");
      }
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <div className="text-6xl mb-4">⏳</div>
            <p className="text-xl text-gray-600">Loading history...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Job Screening History</h1>
          <p className="text-lg text-gray-600">View past job screenings and results</p>
        </div>

        {/* Search Bar and Clear Button */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="flex flex-col md:flex-row gap-4">
            <form onSubmit={handleSearch} className="flex-1 flex gap-4">
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search by job title..."
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
              />
              <button
                type="submit"
                className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
              >
                🔍 Search
              </button>
            </form>
            {history.length > 0 && (
              <button
                onClick={handleClearHistory}
                className="bg-red-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-red-700 transition-colors whitespace-nowrap"
              >
                🗑️ Clear History
              </button>
            )}
          </div>
        </div>

        {/* History List */}
        {history.length === 0 ? (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <div className="text-6xl mb-4">📋</div>
            <h3 className="text-2xl font-bold text-gray-800 mb-2">No History Found</h3>
            <p className="text-gray-600 mb-6">
              {search ? "No results match your search" : "You haven't screened any jobs yet"}
            </p>
            <button
              onClick={() => navigate("/job")}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              Create New Job Description
            </button>
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-lg overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gradient-to-r from-blue-600 to-blue-700 text-white">
                  <tr>
                    <th className="px-6 py-4 text-left text-sm font-semibold">Job Title</th>
                    <th className="px-6 py-4 text-center text-sm font-semibold">Date</th>
                    <th className="px-6 py-4 text-center text-sm font-semibold">Total Resumes</th>
                    <th className="px-6 py-4 text-left text-sm font-semibold">Top Candidate</th>
                    <th className="px-6 py-4 text-center text-sm font-semibold">Highest Score</th>
                    <th className="px-6 py-4 text-center text-sm font-semibold">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {history.map((item) => (
                    <tr key={item.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-6 py-4">
                        <div className="font-semibold text-gray-900">{item.job_title}</div>
                      </td>
                      <td className="px-6 py-4 text-center text-sm text-gray-600">
                        {formatDate(item.created_at)}
                      </td>
                      <td className="px-6 py-4 text-center">
                        <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                          {item.total_resumes}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <div className="text-sm text-gray-700 truncate max-w-xs">
                          {item.top_candidate || "N/A"}
                        </div>
                      </td>
                      <td className="px-6 py-4 text-center">
                        <span className="text-lg font-bold text-green-600">
                          {item.highest_score?.toFixed(2) || "N/A"}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-center">
                        <button
                          onClick={() => navigate(`/history/${item.id}`)}
                          className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-blue-700 transition-colors"
                        >
                          View Details
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default JobHistoryPage;