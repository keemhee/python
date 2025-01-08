'''1. 카메라 켜기
2. model 가져오기(while 위에)
3. model predict(while 안에)
4. result값 받기
5. result.obb.xywhr[0]  ->  angle=result.obb.xywhr[0]  ->  radian_angle=result.obb.xywhr[0], angle=np.degree(radian_angle)
                            cv2.putText(frame,str(ang),(x,y),size,font,scale)

6. 그리퍼 돌리기'''
from ultralytics import YOLO
import cv2
import numpy as np

model = YOLO("yolo11n-obb.pt")

cap = cv2.VideoCapture(0)

while True:
    _,frame = cap.read()
    #frame=cv2.flip(frame,0)

    results = model(frame) 
    
    for result in results:
    #print(result[0].obb.xywhr[0][4])
        r_angle=result.obb.xywhr[0][4]
        angle=np.degrees(r_angle)
        print(angle)
        boxes = result.boxes.xyxy
        classes = result.boxes.cls
        confidences = result.boxes.conf
        for box, cls, conf in zip(boxes, classes, confidences):
            x1, y1, x2, y2 = map(int, box)
            cv2.putText(frame, str(angle), (x1, y1-5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
    

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

    cv2.imshow("yolo obb", frame)

cap.release()
cv2.destroyAllWindows()


#cv2.putText(frame, f"{angle}", points[1], cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)