export async function sendDetectionRequest({ formData, signal }) {
  const res = await fetch("http://localhost:8000/detect", {
    method: "POST",
    body: formData,
    signal,
  });

  if (!res.ok) {
    const t = await res.text();
    throw new Error(t || "Detection failed");
  }

  return res.json();
}

export async function pollProgress(jobId) {
  const res = await fetch(
    `http://localhost:8000/progress?job_id=${encodeURIComponent(jobId)}`
  );
  if (!res.ok) return null;
  return res.json();
}

export async function cancelJobRequest(jobId) {
  await fetch("http://localhost:8000/cancel", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ job_id: jobId }),
  });
}

export async function stopWebcam() {
  await fetch("http://localhost:8000/stop_webcam", {
    method: "POST",
  });
}
