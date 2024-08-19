import React from "react";

const DetectionResults = ({ results }) => {
  return (
    <div className="detection-results">
      {results &&
        results.map((result, index) => (
          <div key={index}>
            <p>{`Object: ${result.label}, Confidence: ${result.confidence}`}</p>
          </div>
        ))}
    </div>
  );
};

export default DetectionResults;
