from ultralytics import YOLO
import cv2
import numpy as np

model = YOLO("yolo11n-obb.pt")

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    results = model(frame) 
    
    for result in results:
        obbs = result.obb.xywhr.cpu().tolist()  # OBB 정보 가져오기
        
        for obb in obbs:
            xc, yc, w, h, angle = obb  # OBB 정보 언패킹
            
            # 라디안을 도로 변환
            angle_deg = np.degrees(angle)
            
            # RotatedRect 객체 생성
            rect = ((xc, yc), (w, h), angle_deg)
            
            # 회전된 사각형의 꼭지점 계산
            box = cv2.boxPoints(rect)
            box = np.int8(box)
            
            # 회전된 사각형 그리기
            cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)
            
            # 각도 텍스트 추가
            cv2.putText(frame, f"Angle: {angle_deg:.2f}", (int(xc), int(yc)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

    cv2.imshow("YOLO OBB", frame)

cap.release()
cv2.destroyAllWindows()