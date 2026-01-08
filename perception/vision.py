import cv2
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def count_people():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return None

    results = model(frame, verbose=False)
    count = 0

    for r in results:
        for box in r.boxes:
            if model.names[int(box.cls[0])] == "person":
                count += 1

    return count
