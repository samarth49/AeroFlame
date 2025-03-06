import React, { useState } from "react";
import axios from "axios";
import { useDropzone } from "react-dropzone";
import { motion } from "framer-motion";
import "./App.css";

function App() {
  const [videoFile, setVideoFile] = useState(null);
  const [videoURL, setVideoURL] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [detectionKey, setDetectionKey] = useState(Date.now()); // Refresh key for fire detection output

  const onDrop = (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      setVideoFile(file);
      setVideoURL(URL.createObjectURL(file)); // Show original video preview
    }
  };

  const { getRootProps, getInputProps } = useDropzone({
    accept: "video/*",
    onDrop,
  });

  const handleUpload = async () => {
    if (!videoFile) {
      alert("Please select a video file first!");
      return;
    }
  
    setUploading(true);
    setError(null);
  
    const formData = new FormData();
    formData.append("file", videoFile);
  
    try {
      await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
  
      setDetectionKey(Date.now()); // Forces React to refresh fire detection output
    } catch (err) {
      setError("Error uploading video. Please try again.");
    } finally {
      setUploading(false);
    }
  };
  
  return (
    <div className="App">
      <h1>🔥 Aero Flame Fire Surveillance Drone</h1>
      <p>Upload a video and let AI detect fire in real-time.</p>

      <div {...getRootProps()} className="drop-zone">
        <input {...getInputProps()} />
        <p>📂 Drag & Drop your video file here, or click to select one.</p>
      </div>

      {videoFile && (
        <motion.button
          className="upload-btn"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleUpload}
          disabled={uploading}
        >
          {uploading ? "Uploading..." : "Upload & Detect"}
        </motion.button>
      )}

      {uploading && <div className="progress-bar"></div>}

      {error && <p className="error">{error}</p>}

      <div className="video-wrapper">
        {/* Original Video Section */}
        <div className="video-box">
          <h3>🎥 Original Video</h3>
          {videoURL && <video src={videoURL} controls />}
        </div>

        {/* Fire Detection Output Section */}
        <div className="video-box">
          <h3>🔥 Fire Detection Output</h3>
          <img
            key={detectionKey} // Forces React to reload the image when new video is uploaded
            src={`http://127.0.0.1:5000/video_feed?timestamp=${detectionKey}`}
            alt="Fire Detection Stream"
          />
        </div>
      </div>
    </div>
  );
}

export default App;
