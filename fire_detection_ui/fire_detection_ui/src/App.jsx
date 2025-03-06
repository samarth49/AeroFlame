import React, { useState } from "react";
import axios from "axios";
import "./App.css"; // Import the CSS file

function App() {
  const [videoFile, setVideoFile] = useState(null);
  const [videoURL, setVideoURL] = useState(null);

  const handleFileChange = (e) => {
    setVideoFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!videoFile) {
      alert("Please select a video file first!");
      return;
    }

    const formData = new FormData();
    formData.append("file", videoFile);

    try {
      setVideoURL(URL.createObjectURL(videoFile));
      await axios.post("http://127.0.0.1:5000/video_feed", formData);
    } catch (error) {
      console.error("Error uploading video:", error);
    }
  };

  return (
    <div className="App">
      <h2>Fire Detection System</h2>

      {/* Custom File Upload Button */}
      <label className="custom-file-upload">
        <input type="file" accept="video/*" onChange={handleFileChange} />
        Choose Video File
      </label>

      <button onClick={handleUpload}>Upload & Detect</button>

      {/* Side-by-side layout for videos */}
      <div className="video-wrapper">
        <div className="video-box">
          <h3>Original Video:</h3>
          {videoURL && <video src={videoURL} controls />}
        </div>

        <div className="video-box">
          <h3>Detection Output:</h3>
          <img src={`http://127.0.0.1:5000/video_feed?timestamp=${new Date().getTime()}`} 
            alt="Fire Detection Stream" />
        </div>
      </div>
    </div>
  );
}

export default App;
