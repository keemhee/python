from roboflow import Roboflow  # Roboflow 라이브러리 임포트
from ultralytics import YOLO  # YOLO 모델을 임포트
import cv2  # OpenCV를 임포트하여 영상 처리를 수행

rf = Roboflow(api_key="znzmK1TZOtY1aYoVFfty")  # Roboflow API 키로 인스턴스 생성
project = rf.workspace("kim-ewj00").project("characters-xxgj0")  # 프로젝트 불러오기
version = project.version(1)  # 프로젝트 버전 설정
dataset = version.download("yolov8")  # 데이터셋 다운로드

model = YOLO('yolov8n.pt')  # YOLO 모델 로드

cap = cv2.VideoCapture(0)  # 웹캠에서 영상을 캡처

while True:  # 무한 루프
    _, frame = cap.read()  # 웹캠으로부터 프레임을 읽음

    results = model(frame)  # 프레임에서 객체를 감지

    x1, y1, x2, y2 = results[0].boxes.xyxy[0]  # 첫 번째 바운딩 박스 좌표 가져오기
    for result in results:  # 감지된 객체들에 대해 반복
        boxes = result.boxes.xyxy  # 바운딩 박스 좌표 가져오기
        classes = result.boxes.cls  # 객체 클래스 가져오기
        confidences = result.boxes.conf  # 객체 신뢰도 가져오기
        names = result.names  # 객체 이름 가져오기
        
        for box, cls, conf in zip(boxes, classes, confidences):  # 각 객체에 대해 반복
            name = names[int(cls)]  # 객체 이름 가져오기
            if names[int(cls)] == 'cup' or names[int(cls)] == 'cell phone':  # 객체가 컵이나 휴대폰인 경우
                x1, y1, x2, y2 = map(int, box)  # 바운딩 박스 좌표를 정수형으로 변환
                cv2.putText(frame, f'{name} {conf:.2f}', (x1, y1-5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)  # 객체 이름과 신뢰도 텍스트 추가
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)  # 바운딩 박스 그리기

    if cv2.waitKey(5) & 0xFF == ord('q'):  # 'q' 키를 누르면 루프 종료
        break

    cv2.imshow("Detecting", frame)  # 결과 프레임을 화면에 표시

cap.release()  # 캡처 객체를 해제
cv2.destroyAllWindows()  # 모든 OpenCV 창을 닫음