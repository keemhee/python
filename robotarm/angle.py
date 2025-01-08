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
ser = serial.Serial('COM3', 9600)  # Replace 'COM3' with your Arduino's port
time.sleep(2)  # Allow time for the serial connection to establish

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

        cv2.circle(frame, (shoulder_x, shoulder_y), 3, (255, 0, 0), -1)
        cv2.circle(frame, (elbow_x, elbow_y), 3, (255, 0, 0), -1)
        cv2.circle(frame, (wrist_x, wrist_y), 3, (255, 0, 0), -1)
        cv2.line(frame, (shoulder_x, shoulder_y), (elbow_x, elbow_y), (0, 255, 0), 2)
        cv2.line(frame, (elbow_x, elbow_y), (wrist_x, wrist_y), (0, 255, 0), 2)

        # Calculate the angle
        angle_e = calculate_angle((shoulder_x, shoulder_y), (elbow_x, elbow_y), (wrist_x, wrist_y))
        angle_str1 = f'{int(angle_e)}'
        print(f'angle1: {angle_str1}')

        # Send angle to Arduino over serial
        ser.write(f"{angle_str1}\n".encode())

        # Show the angle on the video frame
        cv2.putText(frame, angle_str1, (elbow_x, elbow_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    cv2.imshow("Camera", frame)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
serial.close()  # Close the serial connection when done
