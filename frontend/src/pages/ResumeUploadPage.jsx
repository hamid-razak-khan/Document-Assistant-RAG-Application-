import React, { useState, useEffect, useRef, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";
import ResumePreviewModal from "../components/ResumePreviewModal";
import api from "../api/apiClient";

const ResumeUploadPage = () => {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const [resumes, setResumes] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [dragActive, setDragActive] = useState(false);
  const [previewModal, setPreviewModal] = useState(false);
  const [selectedResume, setSelectedResume] = useState(null);
  const fileInputRef = useRef(null);

  const fetchResumes = useCallback(async () => {
    try {
      const res = await api.get(`/jobs/${jobId}/resumes/list/`);
      setResumes(res.data);
    } catch (err) {
      console.error(err);
    }
  }, [jobId]);

  useEffect(() => {
    let intervalId;
    
    // Fetch resumes immediately
    fetchResumes();
    
    // Set up polling with a reasonable interval
    if (!uploading) {
      intervalId = setInterval(() => {
        fetchResumes();
      }, 5000); // Poll every 5 seconds instead of continuously
    }
    
    // Cleanup interval on unmount or when uploading state changes
    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [fetchResumes, uploading]);

  const validateFile = (file) => {
    const allowedTypes = [
      'application/pdf',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'application/msword',
      'text/plain'
    ];
    const allowedExtensions = ['.pdf', '.docx', '.doc', '.txt'];
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    
    return allowedTypes.includes(file.type) || allowedExtensions.includes(fileExtension);
  };

  const handleFilesSelected = async (files) => {
    if (!files || files.length === 0) return;

    // Validate files
    const validFiles = Array.from(files).filter(file => {
      if (!validateFile(file)) {
        alert(`${file.name} is not a supported format. Please upload PDF, DOCX, or TXT files.`);
        return false;
      }
      return true;
    });

    if (validFiles.length === 0) return;

    const formData = new FormData();
    validFiles.forEach((f) => formData.append("files", f));
    
    setUploading(true);
    setProgress(0);

    // Simulate progress
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 90) {
          clearInterval(progressInterval);
          return 90;
        }
        return prev + 10;
      });
    }, 200);

    try {
      const response = await api.post(`/jobs/${jobId}/resumes/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
        // Add timeout and onUploadProgress
        timeout: 60000, // 60 second timeout for file uploads
      });
      
      setProgress(100);
      // Don't call fetchResumes immediately, let the polling handle it
      // await fetchResumes();
      
      // Show success message
      alert(`Successfully uploaded ${response.data.count || validFiles.length} resume(s)!`);
      
      setTimeout(() => {
        setProgress(0);
      }, 1000);
    } catch (err) {
      console.error("Upload error:", err);
      // Provide more specific error messages
      if (err.message) {
        alert(`Upload failed: ${err.message}`);
      } else {
        alert("Upload failed. Please try again.");
      }
    } finally {
      clearInterval(progressInterval);
      setUploading(false);
      // Fetch resumes after upload is complete
      setTimeout(() => {
        fetchResumes();
      }, 1000);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFilesSelected(e.dataTransfer.files);
    }
  };

  const handlePreview = async (resume) => {
    try {
      const res = await api.get(`/resumes/${resume.id}/text/`);
      setSelectedResume(res.data);
      setPreviewModal(true);
    } catch (err) {
      console.error(err);
      alert("Failed to load resume preview");
    }
  };

  const handleProcess = async () => {
    navigate(`/job/${jobId}/results`);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Upload Resumes</h1>
          <p className="text-lg text-gray-600">
            Upload candidate resumes and proceed to screening
          </p>
        </div>

        {/* Drag & Drop Zone */}
        <div
          className={`border-3 border-dashed rounded-xl p-12 mb-8 text-center transition-all duration-200 ${
            dragActive
              ? "border-blue-500 bg-blue-50"
              : "border-gray-300 bg-white hover:border-blue-400 hover:bg-blue-50"
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            ref={fileInputRef}
            type="file"
            multiple
            accept=".pdf,.docx,.doc,.txt"
            onChange={(e) => handleFilesSelected(e.target.files)}
            className="hidden"
          />

          <div className="space-y-4">
            <div className="text-6xl">📤</div>
            <div>
              <p className="text-xl font-semibold text-gray-700 mb-2">
                Drag and drop resume files here
              </p>
              <p className="text-gray-500 mb-4">or</p>
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                disabled={uploading}
                className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                Browse Files
              </button>
            </div>
            <p className="text-sm text-gray-500">
              Supported formats: PDF, DOCX, TXT • Multiple files allowed
            </p>
          </div>
        </div>

        {/* Progress Bar */}
        {uploading && progress > 0 && (
          <div className="mb-8 bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">Uploading...</span>
              <span className="text-sm font-medium text-blue-600">{progress}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
              <div
                className="bg-gradient-to-r from-blue-500 to-blue-600 h-3 rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
        )}

        {/* Uploaded Resumes */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center">
            <span className="text-3xl mr-2">📋</span>
            Uploaded Resumes ({resumes.length})
          </h2>

          {resumes.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <div className="text-6xl mb-4">📁</div>
              <p className="text-lg">No resumes uploaded yet</p>
              <p className="text-sm mt-2">Upload resumes to start screening</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {resumes.map((r) => (
                <div
                  key={r.id}
                  className="border border-gray-200 rounded-lg p-4 hover:shadow-lg transition-shadow duration-200 group"
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center space-x-2 mb-1">
                        <span className="text-2xl">📄</span>
                        <span className="font-semibold text-gray-800 truncate">
                          {r.filename}
                        </span>
                      </div>
                      <div className="text-xs text-gray-500">
                        {new Date(r.uploaded_at).toLocaleString()}
                      </div>
                    </div>
                  </div>

                  <button
                    onClick={() => handlePreview(r)}
                    className="w-full mt-3 bg-blue-50 text-blue-600 px-3 py-2 rounded-md text-sm font-medium hover:bg-blue-100 transition-colors"
                  >
                    Preview Extracted Text
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Action Buttons */}
        <div className="flex gap-4">
          <button
            onClick={() => navigate("/job")}
            className="flex-1 bg-gray-200 text-gray-700 px-6 py-4 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
          >
            ← Back to Job Description
          </button>
          <button
            onClick={handleProcess}
            disabled={!resumes.length || uploading}
            className="flex-1 bg-gradient-to-r from-green-600 to-green-700 text-white px-6 py-4 rounded-lg font-semibold hover:from-green-700 hover:to-green-800 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg"
          >
            {uploading ? "Processing..." : `Process ${resumes.length} Resume${resumes.length !== 1 ? 's' : ''} →`}
          </button>
        </div>
      </div>

      {/* Preview Modal */}
      <ResumePreviewModal
        isOpen={previewModal}
        onClose={() => setPreviewModal(false)}
        resumeData={selectedResume}
      />
    </div>
  );
};

export default ResumeUploadPage;
