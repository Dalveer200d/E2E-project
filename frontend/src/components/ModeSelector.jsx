import { stopWebcam } from "../services/api";

function ModeSelector({ mode, setMode }) {
  const handleChange = async (e) => {
    const nextMode = e.target.value;
    await stopWebcam();     // ✅ stop webcam immediately
    setMode(nextMode);
  };

  return (
    <div className="control-group">
      <label>Detection Mode</label>
      <select value={mode} onChange={handleChange}>
        <option value="image">Image</option>
        <option value="video">Video</option>
        <option value="webcam">Webcam</option>
      </select>
    </div>
  );
}

export default ModeSelector;
