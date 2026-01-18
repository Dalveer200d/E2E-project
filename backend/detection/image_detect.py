import cv2
from pathlib import Path
from utils.model_manager import get_model
from utils.logger import progress, success
from jobs.job_types import JobStatus

def run_image_detection(job, image_path: Path, result_dir: Path, model_size: str):
    job.status = JobStatus.running
    model = get_model(model_size)

    progress(f"[{job.id}] Reading image")
    img = cv2.imread(str(image_path))
    job.progress = 30

    if job.cancelled:
        return

    progress(f"[{job.id}] Running inference")
    results = model(img)
    job.progress = 70

    if job.cancelled:
        return

    annotated = results[0].plot()
    out_path = result_dir / f"{job.id}.jpg"
    cv2.imwrite(str(out_path), annotated)

    job.progress = 100
    job.status = JobStatus.completed
    job.result_url = f"http://localhost:8000/results/{out_path.name}"
    success(f"[{job.id}] Image detection complete")
