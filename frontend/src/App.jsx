import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import JobDescriptionPage from "./pages/JobDescriptionPage";
import ResumeUploadPage from "./pages/ResumeUploadPage";
import ScreeningResultsPage from "./pages/ScreeningResultsPage";
import JobHistoryPage from "./pages/JobHistoryPage";
import JobHistoryDetailsPage from "./pages/JobHistoryDetailsPage";
import "./App.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/job" element={<JobDescriptionPage />} />
        <Route path="/job/:jobId/resumes" element={<ResumeUploadPage />} />
        <Route path="/job/:jobId/results" element={<ScreeningResultsPage />} />
        <Route path="/history" element={<JobHistoryPage />} />
        <Route path="/history/:historyId" element={<JobHistoryDetailsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
