from ultralytics import YOLO

MODEL_MAP = {
    "n": "yolov8n.pt",
    "s": "yolov8s.pt",
    "m": "yolov8m.pt",
    "l": "yolov8l.pt",
}

_model_cache = {}

def get_model(model_size: str):
    if model_size not in MODEL_MAP:
        raise ValueError("Invalid model size")

    if model_size not in _model_cache:
        print(f"[MODEL] Loading {MODEL_MAP[model_size]}")
        _model_cache[model_size] = YOLO(MODEL_MAP[model_size])

    return _model_cache[model_size]
