from ultralytics import YOLO

#yolo detect predict model= yolov8n.pt source=0 show=True
#yolo segment predict model= yolov8n-seg.pt source=0 show=True

import cv2

cap = cv2.VideoCapture(0)

model = YOLO('yolov8n.pt')

while True:
    _,frame = cap.read()

    results = model(frame)

    x1,y1,x2,y2 = results[0].boxes.xyxy[0]
    for result in results:
        boxes = result.boxes.xyxy
        classes = result.boxes.cls
        confidences = result.boxes.conf
        names = result.names
        for box, cls, conf in zip(boxes, classes, confidences):
            name = names[int(cls)]
            if names[int(cls)]=='cup' or names[int(cls)]=='cell phone':
                x1, y1, x2, y2 = map(int, box)
                cv2.putText(frame, f'{name} {conf:.2f}', (x1, y1-5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)


    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

    cv2.imshow("Detecting", frame)

cap.release()
cv2.destroyAllWindows()