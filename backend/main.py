from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import threading

from jobs.job_manager import job_manager
from detection.image_detect import run_image_detection
from detection.video_detect import run_video_detection
from detection.webcam_controller import webcam_controller
from utils.file_utils import save_upload_file
from utils.cleanup import cleanup_session
from utils.logger import info

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
RESULT_DIR = Path("results")
UPLOAD_DIR.mkdir(exist_ok=True)
RESULT_DIR.mkdir(exist_ok=True)

app.mount("/results", StaticFiles(directory=RESULT_DIR), name="results")

@app.post("/detect")
async def detect(
    mode: str = Form(...),
    model_size: str = Form(...),
    file: UploadFile | None = File(None)
):
    webcam_controller.stop()
    cleanup_session(UPLOAD_DIR, RESULT_DIR)

    job = job_manager.create_job()
    info(f"Job {job.id} | mode={mode} | model={model_size}")

    input_path = None
    if file:
        input_path = save_upload_file(file, UPLOAD_DIR)

    if mode == "image":
        threading.Thread(
            target=run_image_detection,
            args=(job, input_path, RESULT_DIR, model_size),
            daemon=True
        ).start()

    elif mode == "video":
        threading.Thread(
            target=run_video_detection,
            args=(job, input_path, RESULT_DIR, model_size),
            daemon=True
        ).start()

    elif mode == "webcam":
        webcam_controller.start(model_size)
        return {"result_url": "http://localhost:8000/stream"}

    return {"job_id": job.id}

@app.get("/progress")
def get_progress(job_id: str):
    job = job_manager.get_job(job_id)
    if not job:
        return {"error": "Invalid job id"}

    return {
        "progress": job.progress,
        "status": job.status,
        "result_url": job.result_url
    }

@app.post("/cancel")
def cancel_job(payload: dict):
    job_id = payload.get("job_id")
    job_manager.cancel_job(job_id)
    webcam_controller.stop()
    cleanup_session(UPLOAD_DIR, RESULT_DIR)
    info(f"Job {job_id} cancelled")
    return {"status": "cancelled"}

@app.post("/stop_webcam")
def stop_webcam():
    webcam_controller.stop()
    cleanup_session(UPLOAD_DIR, RESULT_DIR)
    return {"status": "webcam stopped"}

@app.get("/stream")
def stream():
    return StreamingResponse(
        webcam_controller.generator(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )
