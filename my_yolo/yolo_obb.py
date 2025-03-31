```python
'''1. 카메라 켜기
2. model 가져오기(while 위에)
3. model predict(while 안에)
4. result값 받기
5. result.obb.xywhr[0]  ->  angle=result.obb.xywhr[0]  ->  radian_angle=result.obb.xywhr[0], angle=np.degree(radian_angle)
                            cv2.putText(frame,str(ang),(x,y),size,font,scale)
6. 그리퍼 돌리기'''

from ultralytics import YOLO  # YOLO 모델을 임포트
import cv2  # OpenCV를 임포트하여 영상 처리를 수행
import numpy as np  # NumPy를 임포트하여 수치 연산을 수행

model = YOLO("yolo11n-obb.pt")  # YOLO 모델을 로드

cap = cv2.VideoCapture(0)  # 웹캠에서 영상을 캡처

while True:  # 무한 루프
    _, frame = cap.read()  # 웹캠으로부터 프레임을 읽음
    # frame = cv2.flip(frame, 0)  # (주석 처리됨) 프레임을 수직으로 뒤집음

    results = model(frame)  # 프레임에서 객체를 감지
    
    for result in results:  # 감지된 객체들에 대해 반복
        # print(result[0].obb.xywhr[0][4])  # (주석 처리됨) OBB의 각도 출력
        
        r_angle = result.obb.xywhr[0][4]  # OBB의 각도 가져오기 (라디안 값)
        angle = np.degrees(r_angle)  # 라디안을 도로 변환
        print(angle)  # 각도 출력
        
        boxes = result.boxes.xyxy  # 감지된 객체의 바운딩 박스 좌표 가져오기
        classes = result.boxes.cls  # 감지된 객체의 클래스 가져오기
        confidences = result.boxes.conf  # 감지된 객체의 신뢰도 가져오기
        
        for box, cls, conf in zip(boxes, classes, confidences):  # 각 객체에 대해 반복
            x1, y1, x2, y2 = map(int, box)  # 바운딩 박스 좌표를 정수형으로 변환
            cv2.putText(frame, str(angle), (x1, y1-5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)  # 각도 텍스트 추가
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)  # 바운딩 박스 그리기
    
    if cv2.waitKey(5) & 0xFF == ord('q'):  # 'q' 키를 누르면 루프 종료
        break

    cv2.imshow("yolo obb", frame)  # 결과 프레임을 화면에 표시

cap.release()  # 캡처 객체를 해제
cv2.destroyAllWindows()  # 모든 OpenCV 창을 닫음

# cv2.putText(frame, f"{angle}", points[1], cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)  # (주석 처리됨) 각도를 텍스트로 프레임에 추가
```