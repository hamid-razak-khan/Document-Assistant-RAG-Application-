// src/components/ResultTable.jsx
import React from "react";

const ResultTable = ({ results }) => {
  return (
    <div className="results-table-wrapper">
      <table className="results-table">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Filename</th>
            <th>Final Score</th>
            <th>Skill Match</th>
            <th>Summary</th>
          </tr>
        </thead>
        <tbody>
          {results.map((r, idx) => (
            <tr key={r.resume_id}>
              <td>{idx + 1}</td>
              <td className="candidate-name">{r.filename}</td>
              <td>{r.final_score.toFixed(2)}</td>
              <td>{typeof r.rating === "number" ? r.rating.toFixed(1) : r.rating}</td>
              <td className="summary-cell">{r.summary}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ResultTable;
