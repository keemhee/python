import mediapipe as mp
import cv2
import numpy as np
import serial
import time

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# Initialize the serial communication with Arduino
ser = serial.Serial('COM3', 9600, timeout=2)  # 타임아웃을 2초로 설정

time.sleep(5)  # 5초 대기


mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

while True:

    _, frame = cap.read()

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)

    if results.pose_landmarks:
        shoulder_x = int(results.pose_landmarks.landmark[12].x * frame.shape[1])
        shoulder_y = int(results.pose_landmarks.landmark[12].y * frame.shape[0])
        elbow_x = int(results.pose_landmarks.landmark[14].x * frame.shape[1])
        elbow_y = int(results.pose_landmarks.landmark[14].y * frame.shape[0])
        wrist_x = int(results.pose_landmarks.landmark[16].x * frame.shape[1])
        wrist_y = int(results.pose_landmarks.landmark[16].y * frame.shape[0])

        # 엄지 손가락 위치 추가
        thumb_x = int(results.pose_landmarks.landmark[22].x * frame.shape[1])
        thumb_y = int(results.pose_landmarks.landmark[22].y * frame.shape[0])

        cv2.circle(frame, (shoulder_x, shoulder_y), 3, (255, 0, 0), -1)
        cv2.circle(frame, (elbow_x, elbow_y), 3, (255, 0, 0), -1)
        cv2.circle(frame, (wrist_x, wrist_y), 3, (255, 0, 0), -1)
        cv2.circle(frame, (thumb_x, thumb_y), 3, (255, 0, 0), -1)  # 엄지 손가락 원

        cv2.line(frame, (shoulder_x, shoulder_y), (elbow_x, elbow_y), (0, 255, 0), 2)
        cv2.line(frame, (elbow_x, elbow_y), (wrist_x, wrist_y), (0, 255, 0), 2)
        cv2.line(frame, (wrist_x, wrist_y), (thumb_x, thumb_y), (0, 255, 0), 2)  # 손목과 엄지 연결

        # 팔꿈치와 손목, 엄지 사이의 각도 계산
        angle_e = calculate_angle((shoulder_x, shoulder_y), (elbow_x, elbow_y), (wrist_x, wrist_y))
        angle_str1 = f'{int(angle_e)}'
        print(f'angle1: {angle_str1}')

        # 엄지 손가락 각도 계산
        angle_ew = calculate_angle((elbow_x, elbow_y), (wrist_x, wrist_y), (thumb_x, thumb_y))
        angle_ew = int(np.clip(angle_ew, 0, 180))  # 각도를 0-180 범위로 제한
        angle_str2 = f'{angle_ew}'
        print(f'angle2: {angle_str2}')

        data_to_send = f"{angle_str1},{angle_str2}\n"
        print(f"Sending: {data_to_send.strip()}")
        ser.write(data_to_send.encode())


        # 각도를 아두이노에 전송
        ser.write(f"{angle_str1},{angle_str2}\n".encode())  # angle1과 angle2를 함께 전송
        time.sleep(0.1)  # 잠시 대기하여 안정성 향상

        # 각도를 비디오 프레임에 표시
        cv2.putText(frame, angle_str1, (elbow_x, elbow_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, angle_str2, (wrist_x, wrist_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)  # angle2 표시

    cv2.imshow("Camera", frame)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()  # 종료 시 직렬 연결 닫기
