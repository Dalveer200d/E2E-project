from pathlib import Path
import shutil
from fastapi import UploadFile

def save_upload_file(file: UploadFile, upload_dir: Path) -> Path:
    upload_dir.mkdir(exist_ok=True)
    path = upload_dir / file.filename
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return path
