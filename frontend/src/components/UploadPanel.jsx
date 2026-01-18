function UploadPanel({ mode, modelSize, onRun }) {
  const handleSubmit = (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("mode", mode);
    formData.append("model_size", modelSize); // ✅ CRITICAL FIX

    if (mode !== "webcam") {
      const fileInput = e.target.elements.file;
      if (!fileInput || !fileInput.files.length) {
        alert("Please select a file");
        return;
      }
      formData.append("file", fileInput.files[0]);
    }

    onRun(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="upload-form">
      {mode !== "webcam" && (
        <input
          type="file"
          name="file"
          className="file-input"
          required
        />
      )}

      <button type="submit" className="primary-btn">
        {mode === "webcam" ? "Start Webcam" : "Run Detection"}
      </button>
    </form>
  );
}

export default UploadPanel;
