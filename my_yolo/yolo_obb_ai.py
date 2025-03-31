from ultralytics import YOLO  # YOLO 모델을 임포트
import cv2  # OpenCV를 임포트하여 영상 처리를 수행
import numpy as np  # NumPy를 임포트하여 수치 연산을 수행

model = YOLO("yolo11n-obb.pt")  # YOLO 모델을 로드

cap = cv2.VideoCapture(0)  # 웹캠에서 영상을 캡처

while True:  # 무한 루프
    _, frame = cap.read()  # 웹캠으로부터 프레임을 읽음

    results = model(frame)  # 프레임에서 객체를 감지
    
    for result in results:  # 감지된 객체들에 대해 반복
        obbs = result.obb.xywhr.cpu().tolist()  # OBB 정보 가져오기
        
        for obb in obbs:  # 각 OBB에 대해 반복
            xc, yc, w, h, angle = obb  # OBB 정보 언패킹
            
            angle_deg = np.degrees(angle)  # 라디안을 도로 변환
            
            rect = ((xc, yc), (w, h), angle_deg)  # RotatedRect 객체 생성
            
            box = cv2.boxPoints(rect)  # 회전된 사각형의 꼭지점 계산
            box = np.int8(box)  # 꼭지점 좌표를 정수형으로 변환
            
            cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)  # 회전된 사각형 그리기
            
            cv2.putText(frame, f"Angle: {angle_deg:.2f}", (int(xc), int(yc)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)  # 각도 텍스트 추가

    if cv2.waitKey(5) & 0xFF == ord('q'):  # 'q' 키를 누르면 루프 종료
        break

    cv2.imshow("YOLO OBB", frame)  # 결과 프레임을 화면에 표시

cap.release()  # 캡처 객체를 해제
cv2.destroyAllWindows()  # 모든 OpenCV 창을 닫음