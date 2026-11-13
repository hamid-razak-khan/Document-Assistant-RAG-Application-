import React, { useRef } from "react";

const ResumeDropzone = ({ onFilesSelected }) => {
  const fileInputRef = useRef();

  const handleChange = (e) => {
    const files = Array.from(e.target.files);
    onFilesSelected(files);
  };

  const handleClick = () => fileInputRef.current.click();

  return (
    <div className="dropzone" onClick={handleClick}>
      <p>Drag & Drop Resumes Here</p>
      <p className="subtext">Supported: PDF, Word (doc/docx), Text (txt)</p>
      <input
        ref={fileInputRef}
        type="file"
        multiple
        onChange={handleChange}
        style={{ display: "none" }}
        accept=".pdf,.doc,.docx,.txt"
      />
    </div>
  );
};

export default ResumeDropzone;
