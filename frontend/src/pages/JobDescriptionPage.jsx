import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import api from "../api/apiClient";

const JobDescriptionPage = () => {
  const navigate = useNavigate();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const sampleJobs = [
    {
      title: "Senior Full Stack Developer",
      description: "We are seeking an experienced Full Stack Developer with expertise in React, Node.js, and PostgreSQL. The ideal candidate should have 5+ years of experience in building scalable web applications, strong knowledge of RESTful APIs, microservices architecture, and cloud platforms (AWS/Azure). Experience with Docker, Kubernetes, and CI/CD pipelines is highly preferred."
    },
    {
      title: "Data Scientist",
      description: "Looking for a Data Scientist with strong Python programming skills, experience with machine learning frameworks (TensorFlow, PyTorch, scikit-learn), and proficiency in statistical analysis. Must have experience with data visualization tools, SQL databases, and big data technologies. PhD or Master's degree in Computer Science, Statistics, or related field preferred."
    },
    {
      title: "UI/UX Designer",
      description: "Seeking a creative UI/UX Designer with 3+ years of experience in designing user-centered digital experiences. Proficiency in Figma, Adobe XD, and prototyping tools is required. Must have a strong portfolio demonstrating expertise in responsive design, user research, and usability testing. Experience with design systems and accessibility standards is a plus."
    },
  ];

  const wordCount = description.trim().split(/\s+/).filter(Boolean).length;

  const handleSampleSelect = (sample) => {
    setTitle(sample.title);
    setDescription(sample.description);
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!title.trim()) {
      setError("Job title is required");
      return;
    }

    if (!description.trim()) {
      setError("Job description is required");
      return;
    }

    if (wordCount < 10) {
      setError("Job description must be at least 10 words");
      return;
    }

    setLoading(true);

    try {
      const res = await api.post("/jobs/", { title, text: description });
      const jobId = res.data.id;
      navigate(`/job/${jobId}/resumes`);
    } catch (err) {
      console.error(err);
      setError("Failed to save job description. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Create Job Description</h1>
          <p className="text-lg text-gray-600">
            Define the position and requirements to start screening candidates
          </p>
        </div>

        {/* Sample Job Suggestions */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center">
            <span className="text-2xl mr-2">💡</span>
            Quick Start Templates
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {sampleJobs.map((sample, idx) => (
              <button
                key={idx}
                onClick={() => handleSampleSelect(sample)}
                className="p-4 border-2 border-gray-200 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-all duration-200 text-left group"
              >
                <div className="font-semibold text-gray-800 group-hover:text-blue-600 mb-1">
                  {sample.title}
                </div>
                <div className="text-sm text-gray-500">Click to use template</div>
              </button>
            ))}
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-8">
          {/* Error Message */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 text-red-700 rounded">
              <div className="flex items-center">
                <span className="text-xl mr-2">⚠️</span>
                <span>{error}</span>
              </div>
            </div>
          )}

          {/* Job Title */}
          <div className="mb-6">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Job Title *
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g., Senior Full Stack Developer"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
              required
            />
          </div>

          {/* Job Description */}
          <div className="mb-6">
            <div className="flex justify-between items-center mb-2">
              <label className="block text-sm font-semibold text-gray-700">
                Job Description *
              </label>
              <span className="text-sm text-gray-500">
                {wordCount} words
              </span>
            </div>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Describe the position, required skills, experience level, and qualifications..."
              rows="12"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all resize-none"
              required
            />
            <p className="text-sm text-gray-500 mt-2">
              Provide detailed information about responsibilities, required skills, and qualifications.
              Minimum 10 words required.
            </p>
          </div>

          {/* Submit Button */}
          <div className="flex gap-4">
            <button
              type="submit"
              disabled={loading}
              className="flex-1 bg-gradient-to-r from-blue-600 to-blue-700 text-white px-6 py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-blue-800 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Creating...
                </span>
              ) : (
                "Continue to Upload Resumes →"
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default JobDescriptionPage;
