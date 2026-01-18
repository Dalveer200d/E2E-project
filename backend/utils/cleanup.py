import shutil
from pathlib import Path
from utils.logger import info

def clear_directory(path: Path):
    if not path.exists():
        return
    for item in path.iterdir():
        try:
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        except Exception:
            pass

def cleanup_session(upload_dir: Path, result_dir: Path):
    info("Cleaning up uploads and results")
    clear_directory(upload_dir)
    clear_directory(result_dir)
