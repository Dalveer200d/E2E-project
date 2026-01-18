import cv2
import subprocess
from pathlib import Path
from utils.model_manager import get_model
from utils.logger import progress, success, error
from jobs.job_types import JobStatus

def run_video_detection(job, video_path: Path, result_dir: Path, model_size: str):
    job.status = JobStatus.running
    model = get_model(model_size)

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        error(f"[{job.id}] Cannot open video")
        job.status = JobStatus.error
        return

    ret, first_frame = cap.read()
    if not ret:
        cap.release()
        job.status = JobStatus.error
        return

    h, w = first_frame.shape[:2]
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1

    raw_path = result_dir / f"{job.id}_raw.mp4"
    final_path = result_dir / f"{job.id}.mp4"

    out = cv2.VideoWriter(
        str(raw_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (w, h)
    )

    out.write(model(first_frame)[0].plot())
    frame_idx = 1

    while cap.isOpened():
        if job.cancelled:
            break

        ret, frame = cap.read()
        if not ret:
            break

        out.write(model(frame)[0].plot())
        frame_idx += 1
        job.progress = int((frame_idx / total) * 85)

    cap.release()
    out.release()

    if job.cancelled:
        raw_path.unlink(missing_ok=True)
        job.status = JobStatus.cancelled
        return

    progress(f"[{job.id}] Re-encoding with FFmpeg")

    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(raw_path),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "fast",
            "-movflags", "+faststart",
            str(final_path)
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    raw_path.unlink(missing_ok=True)

    if not final_path.exists():
        job.status = JobStatus.error
        return

    job.progress = 100
    job.status = JobStatus.completed
    job.result_url = f"http://localhost:8000/results/{final_path.name}"
    success(f"[{job.id}] Video detection complete")
