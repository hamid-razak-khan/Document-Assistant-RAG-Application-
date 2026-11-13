import React from "react";

const ResumePreviewModal = ({ isOpen, onClose, resumeData }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="flex min-h-screen items-center justify-center p-4">
        <div className="relative bg-white rounded-lg shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-blue-700 px-6 py-4 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <span className="text-3xl">📄</span>
              <h2 className="text-xl font-bold text-white">Resume Preview</h2>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:text-gray-200 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {/* Content */}
          <div className="p-6 overflow-y-auto max-h-[calc(90vh-80px)]">
            {resumeData ? (
              <>
                {/* Filename */}
                <div className="mb-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
                  <div className="text-sm text-gray-600 mb-1">Filename</div>
                  <div className="font-semibold text-gray-900">{resumeData.filename}</div>
                </div>

                {/* Uploaded Date */}
                {resumeData.uploaded_at && (
                  <div className="mb-6 text-sm text-gray-500">
                    Uploaded: {new Date(resumeData.uploaded_at).toLocaleString()}
                  </div>
                )}

                {/* Extracted Text */}
                <div className="mb-4">
                  <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
                    <span className="text-2xl mr-2">📝</span>
                    Extracted Text
                  </h3>
                  <div className="bg-gray-50 rounded-lg p-6 border border-gray-200">
                    {resumeData.text ? (
                      <pre className="whitespace-pre-wrap font-sans text-sm text-gray-700 leading-relaxed">
                        {resumeData.text}
                      </pre>
                    ) : (
                      <p className="text-gray-500 italic">No text extracted</p>
                    )}
                  </div>
                </div>
              </>
            ) : (
              <div className="text-center py-12">
                <div className="text-6xl mb-4">⏳</div>
                <p className="text-gray-500">Loading resume data...</p>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="bg-gray-50 px-6 py-4 border-t border-gray-200 flex justify-end">
            <button
              onClick={onClose}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResumePreviewModal;
