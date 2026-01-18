import React, { useState, useRef, useEffect } from "react";
import ModeSelector from "./components/ModeSelector";
import ModelSelector from "./components/ModelSelector";
import UploadPanel from "./components/UploadPanel";
import ResultViewer from "./components/ResultViewer";
import LeftPanel from "./components/LeftPanel";
import { sendDetectionRequest, pollProgress, cancelJobRequest } from "./services/api";

function App() {
  const [mode, setMode] = useState("image");
  const [modelSize, setModelSize] = useState("n");
  const [isRunning, setIsRunning] = useState(false);
  const [jobId, setJobId] = useState(null);
  const [progress, setProgress] = useState(0);
  const [statusText, setStatusText] = useState("Idle");
  const [resultUrl, setResultUrl] = useState(null);
  const abortCtrlRef = useRef(null);
  const pollIntervalRef = useRef(null);
  const startTimeRef = useRef(null);

  useEffect(() => {
    return () => {
      // Clean up on unmount
      if (abortCtrlRef.current) abortCtrlRef.current.abort();
      if (pollIntervalRef.current) clearInterval(pollIntervalRef.current);
    };
  }, []);

  const startPolling = (jid) => {
    if (pollIntervalRef.current) clearInterval(pollIntervalRef.current);

    pollIntervalRef.current = setInterval(async () => {
      try {
        const p = await pollProgress(jid);
        if (!p) return;

        const { progress: pct = 0, status = "running", result_url } = p;
        setProgress(pct);
        setStatusText(status);

        if (result_url) {
          setResultUrl(result_url);
        }

        if (status === "completed" || pct >= 100 || result_url) {
          clearInterval(pollIntervalRef.current);
          pollIntervalRef.current = null;
          setIsRunning(false);
          setJobId(null);
          setStatusText("Completed");
        }

        if (status === "cancelled") {
          clearInterval(pollIntervalRef.current);
          pollIntervalRef.current = null;
          setIsRunning(false);
          setJobId(null);
          setStatusText("Cancelled");
        }
      } catch (err) {
        // Keep polling; backend may be warming up
        console.error("Progress poll error:", err);
      }
    }, 800);
  };

  const handleRun = async (formData) => {
    // Reset previous
    setResultUrl(null);
    setProgress(0);
    setStatusText("Starting...");
    setIsRunning(true);
    startTimeRef.current = Date.now();

    // Prepare AbortController for the detect request
    const ac = new AbortController();
    abortCtrlRef.current = ac;

    try {
      const resp = await sendDetectionRequest({
        formData,
        signal: ac.signal,
      });

      // If backend returns immediate result_url
      if (resp?.result_url) {
        setResultUrl(resp.result_url);
        setProgress(100);
        setStatusText("Completed");
        setIsRunning(false);
        abortCtrlRef.current = null;
        return;
      }

      // If backend returns job_id, start polling
      if (resp?.job_id) {
        setJobId(resp.job_id);
        setStatusText("Queued");
        startPolling(resp.job_id);
        return;
      }

      // Unexpected response: try to show result_url if present
      setStatusText("Waiting for server...");
    } catch (err) {
      if (err.name === "AbortError") {
        setStatusText("Cancelled");
      } else {
        console.error("Run request failed:", err);
        setStatusText("Error");
      }
      setIsRunning(false);
      setJobId(null);
      abortCtrlRef.current = null;
    }
  };

  const handleCancel = async () => {
    // Client-side abort
    if (abortCtrlRef.current) {
      try {
        abortCtrlRef.current.abort();
      } catch (e) {
        // ignore
      }
      abortCtrlRef.current = null;
    }

    // If jobId known, request backend cancellation
    if (jobId) {
      try {
        await cancelJobRequest(jobId);
      } catch (err) {
        console.error("Cancel request failed:", err);
      }
    }

    // Stop polling and update UI
    if (pollIntervalRef.current) {
      clearInterval(pollIntervalRef.current);
      pollIntervalRef.current = null;
    }
    setIsRunning(false);
    setJobId(null);
    setStatusText("Cancelled");
  };

  const handleReset = () => {
    // Reset UI to idle
    setIsRunning(false);
    setJobId(null);
    setProgress(0);
    setStatusText("Idle");
    setResultUrl(null);
    if (pollIntervalRef.current) {
      clearInterval(pollIntervalRef.current);
      pollIntervalRef.current = null;
    }
    if (abortCtrlRef.current) {
      try {
        abortCtrlRef.current.abort();
      } catch { }
      abortCtrlRef.current = null;
    }
  };

  return (
    <div className={`app-shell ${isRunning ? "running" : ""}`}>
      <div className={`left-area ${isRunning ? "left-area--collapsed" : ""}`}>
        <div className="glass-card">
          <h1 className="title">Object Detection</h1>
          <p className="subtitle">Adverse weather-ready inference</p>

          {!isRunning && (
            <>
              <ModeSelector mode={mode} setMode={setMode} />
              <ModelSelector modelSize={modelSize} setModelSize={setModelSize} />
              <UploadPanel mode={mode} modelSize={modelSize} onRun={handleRun} />
            </>
          )}

          {isRunning && (
            <LeftPanel
              mode={mode}
              modelSize={modelSize}
              progress={progress}
              statusText={statusText}
              onCancel={handleCancel}
              onReset={handleReset}
            />
          )}
        </div>
      </div>

      <div className="right-area">
        <div className="workspace">
          <div className="workspace-header">
            <div className="status-row">
              <span className="status-label">Status:</span>
              <strong>{statusText}</strong>
              <span className="spacer" />
              <button
                className="small-btn"
                onClick={() => {
                  // quick manual reset
                  handleReset();
                }}
              >
                Reset
              </button>
            </div>
          </div>

          <div className="workspace-body">
            {/* Loader & progress */}
            {isRunning && (
              <div className="processing-pane">
                <div className="loader-visual">
                  <div className="pulse-ring" />
                  <div className="loader-text">Processing</div>
                </div>

                <div className="progress-wrapper">
                  <div className="progress-bar">
                    <div
                      className="progress-fill"
                      style={{ width: `${Math.min(progress, 100)}%` }}
                    />
                  </div>
                  <div className="progress-meta">
                    <div className="percent">{Math.round(progress)}%</div>
                    <div className="eta">Model: {modelSize.toUpperCase()}</div>
                  </div>
                </div>
              </div>
            )}

            {/* Result viewer */}
            <ResultViewer mode={mode} resultUrl={resultUrl} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
