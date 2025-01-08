import mediapipe as mp
import cv2
import numpy as np
import serial

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

arduino = serial.Serial('COM3', 9600)  

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)

    try:
        shoulder_x = int(results.pose_landmarks.landmark[12].x * frame.shape[1])
        shoulder_y = int(results.pose_landmarks.landmark[12].y * frame.shape[0])
        elbow_x = int(results.pose_landmarks.landmark[14].x * frame.shape[1])
        elbow_y = int(results.pose_landmarks.landmark[14].y * frame.shape[0])
        wrist_x = int(results.pose_landmarks.landmark[16].x * frame.shape[1])
        wrist_y = int(results.pose_landmarks.landmark[16].y * frame.shape[0])
        thumb_x = int(results.pose_landmarks.landmark[22].x * frame.shape[1])
        thumb_y = int(results.pose_landmarks.landmark[22].y * frame.shape[0])

        angle_se = calculate_angle((shoulder_x, shoulder_y), (elbow_x, elbow_y), (wrist_x, wrist_y))
        angle_ew = calculate_angle((elbow_x, elbow_y), (wrist_x, wrist_y), (thumb_x, thumb_y))

        angle_se = int(np.clip(angle_se, 0, 180))
        angle_ew = int(np.clip(angle_ew, 0, 180))

        print(f'angle_se: {angle_se}, angle_ew: {angle_ew}')
        
        arduino.write(f"{angle_se},{angle_ew}\n".encode())

    except Exception as e:
        print("Error:", str(e))

    cv2.imshow("Motion Tracking", frame)
        
    if cv2.waitKey(5) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
