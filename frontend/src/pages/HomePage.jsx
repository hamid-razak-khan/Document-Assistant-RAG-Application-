import React from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";

const HomePage = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: "🤖",
      title: "AI-Powered Analysis",
      description: "Uses hybrid TF-IDF, semantic search, and Groq LLM for accurate ranking"
    },
    {
      icon: "⚡",
      title: "Lightning Fast",
      description: "Hash-based embeddings ensure quick processing without GPU requirements"
    },
    {
      icon: "🎯",
      title: "Smart Optimization",
      description: "Top-K LLM analysis saves API costs while maintaining accuracy"
    },
    {
      icon: "📊",
      title: "Detailed Reports",
      description: "Get comprehensive PDF reports with skills match and recommendations"
    },
  ];

  const workflow = [
    {
      step: "1",
      title: "Create Job Description",
      description: "Define the position requirements and desired skills",
      icon: "📝",
      color: "bg-blue-500"
    },
    {
      step: "2",
      title: "Upload Resumes",
      description: "Drag and drop candidate resumes (PDF, DOCX, TXT)",
      icon: "📤",
      color: "bg-green-500"
    },
    {
      step: "3",
      title: "View Rankings",
      description: "Get AI-powered rankings with detailed skill analysis",
      icon: "🏆",
      color: "bg-purple-500"
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      {/* Hero Section */}
      <div className="bg-gradient-to-br from-blue-600 via-blue-700 to-purple-700 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center animate-fade-in">
            <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold mb-6">
              AI Resume Screening Agent
            </h1>
            <p className="text-xl sm:text-2xl mb-4 text-blue-100">
              Smart • Fast • Accurate Hiring
            </p>
            <p className="text-lg sm:text-xl max-w-3xl mx-auto mb-10 text-blue-50">
              Leverage the power of AI to automate resume screening, rank candidates
              intelligently, and make data-driven hiring decisions in minutes.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <button
                onClick={() => navigate("/job")}
                className="bg-white text-blue-700 px-8 py-4 rounded-lg font-semibold text-lg shadow-xl hover:bg-blue-50 transform hover:scale-105 transition-all duration-200 w-64"
              >
                📝 Create Job Description
              </button>
              <button
                onClick={() => navigate("/history")}
                className="bg-blue-800 text-white px-8 py-4 rounded-lg font-semibold text-lg shadow-xl hover:bg-blue-900 transform hover:scale-105 transition-all duration-200 w-64 border-2 border-blue-400"
              >
                📋 View History
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">
          Why Choose Our Platform?
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, idx) => (
            <div
              key={idx}
              className="bg-white p-6 rounded-xl shadow-lg hover:shadow-2xl transition-shadow duration-300 animate-slide-up"
              style={{ animationDelay: `${idx * 0.1}s` }}
            >
              <div className="text-5xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-bold mb-2 text-gray-800">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Workflow Section */}
      <div className="bg-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-4 text-gray-800">
            How It Works
          </h2>
          <p className="text-center text-gray-600 mb-12 text-lg">
            Three simple steps to find your perfect candidate
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {workflow.map((item, idx) => (
              <div key={idx} className="text-center">
                <div className={`${item.color} w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4 text-4xl shadow-lg`}>
                  {item.icon}
                </div>
                <div className={`${item.color} w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-4 text-white font-bold text-xl shadow-md`}>
                  {item.step}
                </div>
                <h3 className="text-xl font-bold mb-2 text-gray-800">{item.title}</h3>
                <p className="text-gray-600">{item.description}</p>
              </div>
            ))}
          </div>

          {/* Start Button */}
          <div className="text-center mt-12">
            <button
              onClick={() => navigate("/job")}
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-10 py-4 rounded-lg font-bold text-xl shadow-xl hover:from-blue-700 hover:to-purple-700 transform hover:scale-105 transition-all duration-200"
            >
              Get Started Now →
            </button>
          </div>
        </div>
      </div>

      {/* Statistics Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold mb-2">Top 3</div>
              <div className="text-blue-100">Candidates get LLM analysis</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">100%</div>
              <div className="text-blue-100">Algorithmic scoring for all</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">Instant</div>
              <div className="text-blue-100">PDF report generation</div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-gray-400">
            © 2024 AI Resume Screening Agent. Powered by Django, React, ChromaDB & Groq.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
