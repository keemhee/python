import mediapipe as mp  # Mediapipe 라이브러리 임포트
import cv2  # OpenCV 라이브러리 임포트
import numpy as np  # NumPy 라이브러리 임포트
import serial  # 시리얼 통신을 위한 라이브러리 임포트
import time  # 시간 관련 함수 사용을 위한 라이브러리 임포트

def calculate_angle(a, b, c):
    a = np.array(a)  # 첫 번째 점의 좌표를 NumPy 배열로 변환
    b = np.array(b)  # 두 번째 점의 좌표를 NumPy 배열로 변환
    c = np.array(c)  # 세 번째 점의 좌표를 NumPy 배열로 변환

    # 각도를 라디안으로 계산
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)  # 라디안을 도 단위로 변환

    if angle > 180.0:
        angle = 360 - angle  # 180도 이상의 각도를 보정

    return angle  # 계산된 각도를 반환

# 아두이노와의 시리얼 통신 초기화
ser = serial.Serial('COM3', 9600)  # 'COM3'를 아두이노의 포트로 변경
time.sleep(2)  # 시리얼 연결이 안정될 때까지 대기

mp_pose = mp.solutions.pose  # Mediapipe의 포즈 솔루션 사용
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)  # 포즈 추적 객체 초기화

cap = cv2.VideoCapture(0)  # 웹캠으로부터 비디오 캡처 객체 생성

while True:

    _, frame = cap.read()  # 비디오 프레임 읽기

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # BGR 이미지를 RGB로 변환
    results = pose.process(img_rgb)  # 포즈 추적 수행

    if results.pose_landmarks:  # 포즈 랜드마크가 감지되었을 때
        shoulder_x = int(results.pose_landmarks.landmark[12].x * frame.shape[1])  # 어깨 X 좌표 계산
        shoulder_y = int(results.pose_landmarks.landmark[12].y * frame.shape[0])  # 어깨 Y 좌표 계산
        elbow_x = int(results.pose_landmarks.landmark[14].x * frame.shape[1])  # 팔꿈치 X 좌표 계산
        elbow_y = int(results.pose_landmarks.landmark[14].y * frame.shape[0])  # 팔꿈치 Y 좌표 계산
        wrist_x = int(results.pose_landmarks.landmark[16].x * frame.shape[1])  # 손목 X 좌표 계산
        wrist_y = int(results.pose_landmarks.landmark[16].y * frame.shape[0])  # 손목 Y 좌표 계산

        cv2.circle(frame, (shoulder_x, shoulder_y), 3, (255, 0, 0), -1)  # 어깨 위치에 원 그리기
        cv2.circle(frame, (elbow_x, elbow_y), 3, (255, 0, 0), -1)  # 팔꿈치 위치에 원 그리기
        cv2.circle(frame, (wrist_x, wrist_y), 3, (255, 0, 0), -1)  # 손목 위치에 원 그리기
        cv2.line(frame, (shoulder_x, shoulder_y), (elbow_x, elbow_y), (0, 255, 0), 2)  # 어깨와 팔꿈치 사이에 선 그리기
        cv2.line(frame, (elbow_x, elbow_y), (wrist_x, wrist_y), (0, 255, 0), 2)  # 팔꿈치와 손목 사이에 선 그리기

        # 각도 계산
        angle_e = calculate_angle((shoulder_x, shoulder_y), (elbow_x, elbow_y), (wrist_x, wrist_y))
        angle_str1 = f'{int(angle_e)}'  # 각도를 문자열로 변환
        print(f'angle1: {angle_str1}')  # 각도 출력

        # 아두이노에 시리얼로 각도 전송
        ser.write(f"{angle_str1}\n".encode())

        # 비디오 프레임에 각도 표시
        cv2.putText(frame, angle_str1, (elbow_x, elbow_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    cv2.imshow("Camera", frame)  # 비디오 프레임을 화면에 표시

    if cv2.waitKey(5) & 0xFF == ord('q'):  # 'q' 키를 누르면 루프 종료
        break

cap.release()  # 비디오 캡처 객체 해제
cv2.destroyAllWindows()  # 모든 OpenCV 윈도우 닫기
serial.close()  # 시리얼 연결 닫기


