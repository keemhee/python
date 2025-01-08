from ultralytics import YOLO
import cv2

model = YOLO("C:/Users/eirmo/Downloads/best.pt")

cap = cv2.VideoCapture(0)

while True:
    _,frame = cap.read()

    results = model(frame)

    #x1,y1,x2,y2 = results[0].boxes.xyxy[0]

   # for result in results:
    #    boxes = result.boxes.xyxy
     #   classes = result.boxes.cls
      #  confidences = result.boxes.conf
       # names = result.names
        #for box, cls, conf in zip(boxes, classes, confidences):
            #name = names[int(cls)]
            #if names[int(cls)]=='shiro' or names[int(cls)]=='doraemon' or names[int(cls)=='pooh']:
                #cv2.putText(frame, f'{name} {conf:.2f}', (x1, y1-5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)
                #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

    cv2.imshow("Detecting", frame)

cap.release()
cv2.destroyAllWindows()
                