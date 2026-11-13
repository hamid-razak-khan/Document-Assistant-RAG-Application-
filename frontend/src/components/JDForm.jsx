import React, { useState } from "react";

const JDForm = ({ onSubmit }) => {
  const [title, setTitle] = useState("");
  const [text, setText] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!text.trim()) return;
    onSubmit({ title: title || "Untitled Role", text });
  };

  return (
    <form onSubmit={handleSubmit} className="form">
      
      <textarea
        className="textarea"
        placeholder="Paste Job Description here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <input
        className="input"
        placeholder="Job Title (optional)"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <button className="btn-primary" type="submit">
        Save JD
      </button>
    </form>
  );
};

export default JDForm;
