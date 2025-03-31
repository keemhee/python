import mediapipe as mp  # Mediapipe 라이브러리 임포트
import cv2  # OpenCV 라이브러리 임포트
import numpy as np  # NumPy 라이브러리 임포트
import serial  # 시리얼 통신을 위한 라이브러리 임포트

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

mp_pose = mp.solutions.pose  # Mediapipe의 포즈 솔루션 사용
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)  # 포즈 추적 객체 초기화

arduino = serial.Serial('COM3', 9600)  # 아두이노와 시리얼 통신 설정 (포트와 속도)

cap = cv2.VideoCapture(0)  # 웹캠으로부터 비디오 캡처 객체 생성

while True:
    _, frame = cap.read()  # 비디오 프레임 읽기
    
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # BGR 이미지를 RGB로 변환
    results = pose.process(img_rgb)  # 포즈 추적 수행

    try:
        # 랜드마크 좌표 추출 및 정수형으로 변환
        shoulder_x = int(results.pose_landmarks.landmark[12].x * frame.shape[1])
        shoulder_y = int(results.pose_landmarks.landmark[12].y * frame.shape[0])
        elbow_x = int(results.pose_landmarks.landmark[14].x * frame.shape[1])
        elbow_y = int(results.pose_landmarks.landmark[14].y * frame.shape[0])
        wrist_x = int(results.pose_landmarks.landmark[16].x * frame.shape[1])
        wrist_y = int(results.pose_landmarks.landmark[16].y * frame.shape[0])
        thumb_x = int(results.pose_landmarks.landmark[22].x * frame.shape[1])
        thumb_y = int(results.pose_landmarks.landmark[22].y * frame.shape[0])

        # 어깨-팔꿈치-손목 사이의 각도 계산
        angle_se = calculate_angle((shoulder_x, shoulder_y), (elbow_x, elbow_y), (wrist_x, wrist_y))
        # 팔꿈치-손목-엄지 사이의 각도 계산
        angle_ew = calculate_angle((elbow_x, elbow_y), (wrist_x, wrist_y), (thumb_x, thumb_y))

        # 0도에서 180도 사이로 각도 제한
        angle_se = int(np.clip(angle_se, 0, 180))
        angle_ew = int(np.clip(angle_ew, 0, 180))

        print(f'angle_se: {angle_se}, angle_ew: {angle_ew}')  # 각도 출력
        
        arduino.write(f"{angle_se},{angle_ew}\n".encode())  # 필터링된 각도를 아두이노에 시리얼로 전송

    except Exception as e:
        print("Error:", str(e))  # 에러 메시지 출력

    cv2.imshow("Motion Tracking", frame)  # 비디오 프레임을 화면에 표시
    
    if cv2.waitKey(5) & 0xff == ord('q'):  # 'q' 키를 누르면 루프 종료
        break

cap.release()  # 비디오 캡처 객체 해제
cv2.destroyAllWindows()  # 모든 OpenCV 윈도우 닫기
arduino.close()  # 시리얼 연결 닫기