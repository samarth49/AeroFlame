from ultralytics import YOLO
import cvzone
import cv2
import math

# Load the YOLO model
model = YOLO('fire.pt')

# Open video file
cap = cv2.VideoCapture('fire2.mp4')

# Class names
classnames = ['fire']

while True:
    ret, frame = cap.read()

    # Check if frame was read successfully
    if not ret:
        print("Video ended or error reading frame.")
        break

    # Resize frame
    frame = cv2.resize(frame, (640, 480))

    # Perform inference
    results = model(frame, stream=True)

    # Loop through detections
    for info in results:
        boxes = info.boxes
        for box in boxes:
            confidence = box.conf.item() * 100  # Convert to scalar
            confidence = math.ceil(confidence)

            class_id = int(box.cls.item())  # Convert class index to int
            if confidence > 50:
                # Get bounding box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Draw bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)

                # Put label text with confidence
                cvzone.putTextRect(frame, f'{classnames[class_id]} {confidence}%', 
                                   (x1 + 8, y1 - 10), scale=1.5, thickness=2, colorR=(255, 0, 0))

    # Display the frame
    cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
    cv2.imshow('frame', frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
