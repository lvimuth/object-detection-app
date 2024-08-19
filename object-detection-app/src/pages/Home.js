import React, { useState } from "react";
import FileUpload from "../components/FileUpload";
import DetectionResults from "../components/DetectionResults";

const Home = () => {
  const [results, setResults] = useState([]);

  const handleFileUpload = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:5000/detect", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setResults(data.results);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="home">
      <h1>Object Detection App</h1>
      <FileUpload onFileUpload={handleFileUpload} />
      <DetectionResults results={results} />
    </div>
  );
};

export default Home;
