import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import api from "../api/apiClient";

const ScreeningResultsPage = () => {
  const { jobId } = useParams();
  const [job, setJob] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [topN, setTopN] = useState(5);
  const [expandedRow, setExpandedRow] = useState(null);
  const navigate = useNavigate();
  
  // Email modal state
  const [showEmailModal, setShowEmailModal] = useState(false);
  const [emailMode, setEmailMode] = useState("top_n");
  const [topNEmail, setTopNEmail] = useState(3);
  const [scoreThreshold, setScoreThreshold] = useState(75);
  const [selectedIds, setSelectedIds] = useState([]);
  const [customMessage, setCustomMessage] = useState("");
  const [sendingEmail, setSendingEmail] = useState(false);
  const [emailResult, setEmailResult] = useState(null);
  const [previewCandidates, setPreviewCandidates] = useState([]);
  const [showPreview, setShowPreview] = useState(false);
  const [previewLoading, setPreviewLoading] = useState(false);

  useEffect(() => {
    const loadResults = async () => {
      setLoading(true);
      try {
        const res = await api.post(`/jobs/${jobId}/rank/`);
        setJob(res.data.job);
        setResults(res.data.results);
      } catch (e) {
        console.error(e);
        alert("Error fetching results");
      } finally {
        setLoading(false);
      }
    };
    loadResults();
  }, [jobId]);

  const getScoreColor = (score) => {
    if (score >= 70) return "text-green-600";
    if (score >= 50) return "text-yellow-600";
    return "text-red-600";
  };

  const getRankBadge = (rank) => {
    if (rank === 0) return "bg-yellow-400 text-yellow-900 shadow-md";
    if (rank === 1) return "bg-gray-300 text-gray-800 shadow-md";
    if (rank === 2) return "bg-orange-400 text-orange-900 shadow-md";
    return "bg-blue-100 text-blue-800";
  };

  const displayedResults = results.slice(0, topN);

  // Preview candidates before sending email
  const handlePreviewEmail = async () => {
    setPreviewLoading(true);
    setPreviewCandidates([]);
    
    try {
      let requestData = {
        mode: emailMode
      };
      
      if (emailMode === "top_n") {
        requestData.count = topNEmail;
      } else if (emailMode === "score_threshold") {
        requestData.score = scoreThreshold;
      } else if (emailMode === "selected") {
        // Map displayed results to their resume IDs
        const ids = selectedIds.map(id => parseInt(id));
        requestData.resume_ids = ids;
      }
      
      const response = await api.post("/preview-bulk-email/", requestData);
      setPreviewCandidates(response.data.candidates);
      setShowPreview(true);
    } catch (error) {
      console.error("Error previewing candidates:", error);
      alert("Failed to preview candidates. Please try again.");
    } finally {
      setPreviewLoading(false);
    }
  };

  // Handle sending bulk emails
  const handleSendEmail = async () => {
    setSendingEmail(true);
    setEmailResult(null);
    
    try {
      let requestData = {
        mode: emailMode,
        message: customMessage
      };
      
      if (emailMode === "top_n") {
        requestData.count = topNEmail;
      } else if (emailMode === "score_threshold") {
        requestData.score = scoreThreshold;
      } else if (emailMode === "selected") {
        // Map displayed results to their resume IDs
        const ids = selectedIds.map(id => parseInt(id));
        requestData.resume_ids = ids;
      }
      
      const response = await api.post("/send-bulk-email/", requestData);
      setEmailResult(response.data);
      alert(`Emails sent successfully! Sent: ${response.data.total_sent}, Skipped: ${response.data.total_skipped}`);
      
      // Close modal after successful send
      setShowEmailModal(false);
    } catch (error) {
      console.error("Error sending emails:", error);
      alert("Failed to send emails. Please try again.");
    } finally {
      setSendingEmail(false);
    }
  };

  // Toggle selection of a candidate
  const toggleSelection = (resumeId) => {
    if (selectedIds.includes(resumeId.toString())) {
      setSelectedIds(selectedIds.filter(id => id !== resumeId.toString()));
    } else {
      setSelectedIds([...selectedIds, resumeId.toString()]);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <div className="text-6xl mb-4">⏳</div>
            <p className="text-xl text-gray-600">Analyzing resumes with AI...</p>
            <p className="text-sm text-gray-500 mt-2">This may take a few moments</p>
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
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Screening Results</h1>
          {job && <p className="text-xl text-gray-600">{job.title}</p>}
          <p className="text-sm text-gray-500 mt-2">Total Candidates: {results.length}</p>
        </div>

        {/* Top 3 Podium */}
        {results.length >= 3 && (
          <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">🏆 Top 3 Candidates</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {results.slice(0, 3).map((r, i) => (
                <div
                  key={r.resume_id}
                  className={`border-2 rounded-xl p-6 ${getRankBadge(i)} transition-all hover:scale-105`}
                >
                  <div className="text-center mb-4">
                    <div className="text-4xl mb-2">
                      {i === 0 ? "🥇" : i === 1 ? "🥈" : "🥉"}
                    </div>
                    <div className="font-bold text-lg mb-1">#{i + 1}</div>
                  </div>
                  <div className="text-sm font-semibold mb-2 truncate">{r.filename}</div>
                  <div className="text-2xl font-bold mb-2">{r.final_score.toFixed(2)}</div>
                  {r.llm_analyzed && (
                    <div className="text-xs bg-white bg-opacity-50 rounded px-2 py-1 inline-block">
                      ✓ LLM Analyzed
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Controls */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div className="flex items-center space-x-3">
              <label className="text-sm font-semibold text-gray-700">Show Top:</label>
              <select
                value={topN}
                onChange={(e) => setTopN(Number(e.target.value))}
                className="border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 outline-none"
              >
                {[1, 3, 5, 10, 15, 20, results.length].map((n) => (
                  <option key={n} value={n}>
                    {n === results.length ? `All (${n})` : n}
                  </option>
                ))}
              </select>
              <span className="text-sm text-gray-500">candidates</span>
            </div>
            <div className="flex gap-3">
              <button
                onClick={() => setShowEmailModal(true)}
                className="bg-green-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-green-700 transition-colors"
              >
                📧 Send Email
              </button>
              <button
                onClick={() => navigate("/job")}
                className="bg-gray-200 text-gray-700 px-6 py-2 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
              >
                New Search
              </button>
            </div>
          </div>
        </div>

        {/* Results Table */}
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gradient-to-r from-blue-600 to-blue-700 text-white">
                <tr>
                  {emailMode === "selected" && (
                    <th className="px-6 py-4 text-center text-sm font-semibold">Select</th>
                  )}
                  <th className="px-6 py-4 text-left text-sm font-semibold">Rank</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold">Candidate</th>
                  <th className="px-6 py-4 text-center text-sm font-semibold">Final Score</th>
                  <th className="px-6 py-4 text-center text-sm font-semibold">Keyword</th>
                  <th className="px-6 py-4 text-center text-sm font-semibold">Semantic</th>
                  <th className="px-6 py-4 text-center text-sm font-semibold">Status</th>
                  <th className="px-6 py-4 text-center text-sm font-semibold">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {displayedResults.map((r, i) => (
                  <React.Fragment key={r.resume_id}>
                    <tr className={`hover:bg-gray-50 transition-colors ${i < 3 ? "bg-blue-50" : ""}`}>
                      {emailMode === "selected" && (
                        <td className="px-6 py-4 text-center">
                          <input
                            type="checkbox"
                            checked={selectedIds.includes(r.resume_id.toString())}
                            onChange={() => toggleSelection(r.resume_id)}
                            className="h-5 w-5 text-blue-600 rounded focus:ring-blue-500"
                          />
                        </td>
                      )}
                      <td className="px-6 py-4">
                        <div className={`inline-flex items-center justify-center w-8 h-8 rounded-full font-bold text-sm ${getRankBadge(i)}`}>
                          {i + 1}
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="font-semibold text-gray-900">{r.filename}</div>
                      </td>
                      <td className="px-6 py-4 text-center">
                        <div className={`text-2xl font-bold ${getScoreColor(r.final_score)}`}>
                          {r.final_score.toFixed(2)}
                        </div>
                      </td>
                      <td className="px-6 py-4 text-center">
                        <div className="text-sm text-gray-600">{r.keyword_score.toFixed(2)}</div>
                      </td>
                      <td className="px-6 py-4 text-center">
                        <div className="text-sm text-gray-600">{r.semantic_score.toFixed(2)}</div>
                      </td>
                      <td className="px-6 py-4 text-center">
                        {r.llm_analyzed ? (
                          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                            ✓ LLM Analyzed
                          </span>
                        ) : (
                          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700">
                            ⚡ Algorithm Only
                          </span>
                        )}
                      </td>
                      <td className="px-6 py-4 text-center">
                        <button
                          onClick={() => setExpandedRow(expandedRow === i ? null : i)}
                          className="text-blue-600 hover:text-blue-800 font-medium text-sm"
                        >
                          {expandedRow === i ? "Hide Details" : "View Details"}
                        </button>
                      </td>
                    </tr>
                    {expandedRow === i && (
                      <tr>
                        <td colSpan={emailMode === "selected" ? "8" : "7"} className="px-6 py-6 bg-gray-50">
                          <div className="space-y-4">
                            <div>
                              <h4 className="font-semibold text-gray-800 mb-2">Summary</h4>
                              <p className="text-gray-700 text-sm">{r.summary}</p>
                            </div>
                            {r.llm_analyzed && (
                              <>
                                <div>
                                  <h4 className="font-semibold text-gray-800 mb-2">Matching Skills</h4>
                                  <div className="flex flex-wrap gap-2">
                                    {Array.isArray(r.matching_skills) && r.matching_skills.length > 0 ? (
                                      r.matching_skills.map((skill, idx) => (
                                        <span key={idx} className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-xs font-medium">
                                          ✓ {skill}
                                        </span>
                                      ))
                                    ) : (
                                      <span className="text-gray-500 text-sm">None identified</span>
                                    )}
                                  </div>
                                </div>
                                <div>
                                  <h4 className="font-semibold text-gray-800 mb-2">Missing Skills</h4>
                                  <div className="flex flex-wrap gap-2">
                                    {Array.isArray(r.missing_skills) && r.missing_skills.length > 0 ? (
                                      r.missing_skills.map((skill, idx) => (
                                        <span key={idx} className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-xs font-medium">
                                          ✗ {skill}
                                        </span>
                                      ))
                                    ) : (
                                      <span className="text-gray-500 text-sm">None identified</span>
                                    )}
                                  </div>
                                </div>
                                {r.rating !== null && r.rating !== undefined && (
                                  <div>
                                    <h4 className="font-semibold text-gray-800 mb-2">Skill Match Rating</h4>
                                    <div className="flex items-center space-x-3">
                                      <div className="flex-1 bg-gray-200 rounded-full h-4">
                                        <div
                                          className="bg-gradient-to-r from-blue-500 to-blue-600 h-4 rounded-full transition-all"
                                          style={{ width: `${r.rating}%` }}
                                        />
                                      </div>
                                      <span className="font-bold text-blue-600">{r.rating}%</span>
                                    </div>
                                  </div>
                                )}
                              </>
                            )}
                          </div>
                        </td>
                      </tr>
                    )}
                  </React.Fragment>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Email Modal */}
      {showEmailModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-bold text-gray-900">Send Bulk Email</h3>
                <button
                  onClick={() => setShowEmailModal(false)}
                  className="text-gray-500 hover:text-gray-700 text-2xl"
                >
                  &times;
                </button>
              </div>

              {!showPreview ? (
                <div className="space-y-6">
                  {/* Email Mode Selection */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Send Email To:
                    </label>
                    <div className="space-y-2">
                      <label className="flex items-center">
                        <input
                          type="radio"
                          name="emailMode"
                          value="top_n"
                          checked={emailMode === "top_n"}
                          onChange={(e) => setEmailMode(e.target.value)}
                          className="h-4 w-4 text-blue-600"
                        />
                        <span className="ml-2">Top N candidates</span>
                      </label>
                      
                      <label className="flex items-center">
                        <input
                          type="radio"
                          name="emailMode"
                          value="score_threshold"
                          checked={emailMode === "score_threshold"}
                          onChange={(e) => setEmailMode(e.target.value)}
                          className="h-4 w-4 text-blue-600"
                        />
                        <span className="ml-2">Candidates with final score ≥ X</span>
                      </label>
                      
                      <label className="flex items-center">
                        <input
                          type="radio"
                          name="emailMode"
                          value="selected"
                          checked={emailMode === "selected"}
                          onChange={(e) => setEmailMode(e.target.value)}
                          className="h-4 w-4 text-blue-600"
                        />
                        <span className="ml-2">Selected candidates (check boxes in table)</span>
                      </label>
                    </div>
                  </div>

                  {/* Mode-specific inputs */}
                  {emailMode === "top_n" && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Number of Top Candidates:
                      </label>
                      <input
                        type="number"
                        min="1"
                        value={topNEmail}
                        onChange={(e) => setTopNEmail(parseInt(e.target.value) || 1)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                  )}

                  {emailMode === "score_threshold" && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Minimum Score Threshold:
                      </label>
                      <input
                        type="number"
                        min="0"
                        max="100"
                        value={scoreThreshold}
                        onChange={(e) => setScoreThreshold(parseInt(e.target.value) || 0)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>
                  )}

                  {emailMode === "selected" && (
                    <div className="bg-blue-50 p-4 rounded-md">
                      <p className="text-sm text-blue-800">
                        Select candidates by checking the boxes in the table above, then click "Preview Candidates".
                      </p>
                      <p className="text-sm text-blue-700 mt-1">
                        Selected candidates: {selectedIds.length}
                      </p>
                    </div>
                  )}

                  {/* Custom Message */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Custom Email Message:
                    </label>
                    <textarea
                      value={customMessage}
                      onChange={(e) => setCustomMessage(e.target.value)}
                      rows={6}
                      placeholder="Enter your custom email message here..."
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  {/* Action Buttons */}
                  <div className="flex justify-end space-x-3">
                    <button
                      onClick={() => setShowEmailModal(false)}
                      disabled={previewLoading || sendingEmail}
                      className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 disabled:opacity-50"
                    >
                      Cancel
                    </button>
                    <button
                      onClick={handlePreviewEmail}
                      disabled={previewLoading || sendingEmail}
                      className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 flex items-center"
                    >
                      {previewLoading ? (
                        <>
                          <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          Previewing...
                        </>
                      ) : (
                        "Preview Candidates"
                      )}
                    </button>
                  </div>
                </div>
              ) : (
                <div className="space-y-6">
                  <h3 className="text-lg font-semibold text-gray-900">Preview Candidates ({previewCandidates.length})</h3>
                  
                  {/* Candidates List */}
                  <div className="max-h-60 overflow-y-auto border border-gray-200 rounded-md">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Candidate</th>
                          <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Score</th>
                          <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {previewCandidates.map((candidate, index) => (
                          <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                            <td className="px-4 py-2 text-sm text-gray-900">{candidate.candidate}</td>
                            <td className="px-4 py-2 text-sm text-gray-900">{candidate.score.toFixed(2)}</td>
                            <td className="px-4 py-2 text-sm">
                              {candidate.email ? (
                                <span className="text-green-600">{candidate.email}</span>
                              ) : (
                                <span className="text-red-600">No email found</span>
                              )}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                  
                  {/* Stats */}
                  <div className="bg-gray-50 p-4 rounded-md">
                    <div className="grid grid-cols-3 gap-4 text-center">
                      <div>
                        <p className="text-sm text-gray-500">Total Candidates</p>
                        <p className="text-xl font-bold text-gray-900">{previewCandidates.length}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-500">With Emails</p>
                        <p className="text-xl font-bold text-green-600">
                          {previewCandidates.filter(c => c.email).length}
                        </p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-500">Without Emails</p>
                        <p className="text-xl font-bold text-red-600">
                          {previewCandidates.filter(c => !c.email).length}
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  {/* Action Buttons */}
                  <div className="flex justify-between">
                    <button
                      onClick={() => setShowPreview(false)}
                      disabled={sendingEmail}
                      className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 disabled:opacity-50"
                    >
                      Back to Settings
                    </button>
                    <div className="flex space-x-3">
                      <button
                        onClick={() => setShowEmailModal(false)}
                        disabled={sendingEmail}
                        className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 disabled:opacity-50"
                      >
                        Cancel
                      </button>
                      <button
                        onClick={handleSendEmail}
                        disabled={sendingEmail || !customMessage.trim()}
                        className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 flex items-center"
                      >
                        {sendingEmail ? (
                          <>
                            <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Sending...
                          </>
                        ) : (
                          "Send Email Now"
                        )}
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ScreeningResultsPage;