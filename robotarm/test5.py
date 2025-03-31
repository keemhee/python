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
ser = serial.Serial('COM3', 9600, timeout=2)  # 타임아웃을 2초로 설정

time.sleep(5)  # 5초 대기

mp_pose = mp.solutions.pose  # Mediapipe의 포즈 솔루션 사용
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)  # 포즈 추적 객체 초기화

cap = cv2.VideoCapture(0)  # 웹캠으로부터 비디오 캡처 객체 생성

while True:
    _, frame = cap.read()  # 비디오 프레임 읽기
    
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # BGR 이미지를 RGB로 변환
    results = pose.process(img_rgb)  # 포즈 추적 수행

    if results.pose_landmarks:  # 포즈 랜드마크가 감지되었을 때
        # 랜드마크 좌표 추출 및 정수형으로 변환
        shoulder_x = int(results.pose_landmarks.landmark[12].x * frame.shape[1])
        shoulder_y = int(results.pose_landmarks.landmark[12].y * frame.shape[0])
        elbow_x = int(results.pose_landmarks.landmark[14].x * frame.shape[1])
        elbow_y = int(results.pose_landmarks.landmark[14].y * frame.shape[0])
        wrist_x = int(results.pose_landmarks.landmark[16].x * frame.shape[1])
        wrist_y = int(results.pose_landmarks.landmark[16].y * frame.shape[0])
        thumb_x = int(results.pose_landmarks.landmark[22].x * frame.shape[1])
        thumb_y = int(results.pose_landmarks.landmark[22].y * frame.shape[0])

        # 랜드마크 위치에 원 그리기
        cv2.circle(frame, (shoulder_x, shoulder_y), 3, (255, 0, 0), -1)
        cv2.circle(frame, (elbow_x, elbow_y), 3, (255, 0, 0), -1)
        cv2.circle(frame, (wrist_x, wrist_y), 3, (255, 0, 0), -1)
        cv2.circle(frame, (thumb_x, thumb_y), 3, (255, 0, 0), -1)  # 엄지 손가락 원
        # 랜드마크 사이에 선 그리기
        cv2.line(frame, (shoulder_x, shoulder_y), (elbow_x, elbow_y), (0, 255, 0), 2)
        cv2.line(frame, (elbow_x, elbow_y), (wrist_x, wrist_y), (0, 255, 0), 2)
        cv2.line(frame, (wrist_x, wrist_y), (thumb_x, thumb_y), (0, 255, 0), 2)  # 손목과 엄지 연결

        # 어깨-팔꿈치-손목 사이의 각도 계산
        angle_e = calculate_angle((shoulder_x, shoulder_y), (elbow_x, elbow_y), (wrist_x, wrist_y))
        angle_str1 = f'{int(angle_e)}'  # 각도를 문자열로 변환
        print(f'angle1: {angle_str1}')  # 각도 출력

        # 팔꿈치-손목-엄지 사이의 각도 계산
        angle_ew = calculate_angle((elbow_x, elbow_y), (wrist_x, wrist_y), (thumb_x, thumb_y))
        angle_ew = int(np.clip(angle_ew, 0, 180))  # 각도를 0-180 범위로 제한
        angle_str2 = f'{angle_ew}'  # 각도를 문자열로 변환
        print(f'angle2: {angle_str2}')  # 각도 출력

        data_to_send = f"{angle_str1},{angle_str2}\n"  # 전송할 데이터 문자열 생성
        print(f"Sending: {data_to_send.strip()}")  # 전송할 데이터 출력
        ser.write(data_to_send.encode())  # 데이터를 시리얼로 전송

        # 각도를 비디오 프레임에 표시
        cv2.putText(frame, angle_str1, (elbow_x, elbow_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, angle_str2, (wrist_x, wrist_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)  # angle2 표시

    cv2.imshow("Camera", frame)  # 비디오 프레임을 화면에 표시

    if cv2.waitKey(5) & 0xFF == ord('q'):  # 'q' 키를 누르면 루프 종료
        break

cap.release()  # 비디오 캡처 객체 해제
cv2.destroyAllWindows()  # 모든 OpenCV 윈도우 닫기
ser.close()  # 종료 시 시리얼 연결 닫기