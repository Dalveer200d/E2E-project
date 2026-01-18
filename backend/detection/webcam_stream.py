# import cv2
# from utils.model_manager import get_model

# def webcam_generator(model_size: str):
#     model = get_model(model_size)
#     cap = cv2.VideoCapture(0)

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         results = model(frame)
#         annotated = results[0].plot()

#         _, buffer = cv2.imencode(".jpg", annotated)
#         yield (
#             b"--frame\r\n"
#             b"Content-Type: image/jpeg\r\n\r\n" +
#             buffer.tobytes() +
#             b"\r\n"
#         )
