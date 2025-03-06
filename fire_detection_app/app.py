from flask import Flask, request, Response
import cv2
import os
from ultralytics import YOLO
import cvzone
import math
import threading
import time

app = Flask(__name__)

# Load YOLO fire detection model
model = YOLO("fire.pt")

# Storage path for uploaded videos
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

cap = None  # Global video capture object
processing = False  # Control flag for video processing
lock = threading.Lock()  # Ensure thread safety


@app.route("/upload", methods=["POST"])
def upload_video():
    global cap, processing

    with lock:
        # Stop any existing video processing
        processing = False
        time.sleep(1)  # Give some time for the process to stop

        # Remove previous video before saving new one
        for file in os.listdir(UPLOAD_FOLDER):
            os.remove(os.path.join(UPLOAD_FOLDER, file))

        video_file = request.files["file"]
        video_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
        video_file.save(video_path)

        # Load new video for processing
        cap = cv2.VideoCapture(video_path)
        processing = True  # Start processing the new video

    return {"message": "Video uploaded successfully!"}


def generate_frames():
    global cap, processing
    while True:
        with lock:
            if not processing or cap is None:
                time.sleep(0.1)  # Prevents busy waiting
                continue

            success, frame = cap.read()
            if not success:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video loop
                continue

            frame = cv2.resize(frame, (640, 480))

            # Perform YOLO inference
            results = model(frame, stream=True)

            for info in results:
                boxes = info.boxes
                for box in boxes:
                    confidence = math.ceil(box.conf.item() * 100)
                    class_id = int(box.cls.item())
                    if confidence > 50:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                        cvzone.putTextRect(frame, f'Fire {confidence}%', 
                                           (x1 + 5, y1 - 10), scale=1, thickness=2, colorR=(255, 0, 0))

            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
