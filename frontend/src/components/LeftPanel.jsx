function LeftPanel({
  mode,
  modelSize,
  progress,
  statusText,
  onCancel,
  onReset,
}) {
  return (
    <div className="left-panel-running">
      <div className="left-panel-header">
        <h3>Running Job</h3>
        <div className="sub">
          {mode.toUpperCase()} · YOLOv8-{modelSize.toUpperCase()}
        </div>
      </div>

      <div className="panel-row">
        <label>Progress</label>
        <div className="small-progress">
          <div
            className="small-fill"
            style={{ width: `${Math.min(progress, 100)}%` }}
          />
        </div>
      </div>

      <div className="status-box">{statusText}</div>

      <div className="panel-actions">
        <button className="cancel-btn" onClick={onCancel}>
          Cancel
        </button>
        <button className="tertiary-btn" onClick={onReset}>
          Reset
        </button>
      </div>
    </div>
  );
}

export default LeftPanel;
