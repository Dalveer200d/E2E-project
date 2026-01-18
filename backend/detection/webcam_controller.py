import cv2
from threading import Lock
from utils.model_manager import get_model

class WebcamController:
    def __init__(self):
        self.cap = None
        self.running = False
        self.model_size = None
        self.lock = Lock()

    def start(self, model_size: str):
        with self.lock:
            if self.running:
                return
            self.cap = cv2.VideoCapture(0)
            self.model_size = model_size
            self.running = True

    def stop(self):
        with self.lock:
            self.running = False
            if self.cap:
                self.cap.release()
                self.cap = None

    def generator(self):
        model = get_model(self.model_size)
        while True:
            with self.lock:
                if not self.running or self.cap is None:
                    break
                cap = self.cap

            ret, frame = cap.read()
            if not ret:
                break

            annotated = model(frame)[0].plot()
            _, buffer = cv2.imencode(".jpg", annotated)

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" +
                buffer.tobytes() +
                b"\r\n"
            )

        self.stop()

webcam_controller = WebcamController()
