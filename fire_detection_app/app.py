from flask import Flask, Response
import cv2
from ultralytics import YOLO
import cvzone
import math

app = Flask(__name__)

# Load YOLO fire detection model
model = YOLO("fire.pt")

# Open video file
cap = cv2.VideoCapture("fire2.mp4")

classnames = ["fire"]

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            # Reset video capture to loop the video
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue  # Skip iteration and retry

        frame = cv2.resize(frame, (640, 480))

        # Perform YOLO inference
        results = model(frame, stream=True)

        for info in results:
            boxes = info.boxes
            for box in boxes:
                confidence = math.ceil(box.conf.item() * 100)  # Convert to scalar
                class_id = int(box.cls.item())  # Convert class index to int
                if confidence > 50:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    cvzone.putTextRect(frame, f'{classnames[class_id]} {confidence}%', 
                                       (x1 + 5, y1 - 10), scale=1, thickness=2, colorR=(255, 0, 0))

        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)  # Disable debug mode to prevent restarts
