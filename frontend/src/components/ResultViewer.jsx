function ResultViewer({ mode, resultUrl }) {
  if (!resultUrl) {
    return (
      <div className="result-placeholder">
        <div className="placeholder-inner">
          No result yet. Run detection to see output.
        </div>
      </div>
    );
  }

  if (mode === "image") {
    return (
      <div className="result-container">
        <img src={resultUrl} alt="Detection result" className="result-media" />
      </div>
    );
  }

  if (mode === "video") {
    return (
      <div className="result-container">
        <video
          src={resultUrl}
          controls
          className="result-media"
        />
      </div>
    );
  }

  if (mode === "webcam") {
    return (
      <div className="result-container">
        <img
          src={resultUrl}
          alt="Webcam stream"
          className="result-media"
        />
      </div>
    );
  }

  return null;
}

export default ResultViewer;
