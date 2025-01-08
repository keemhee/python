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

# Kalman filter variables
angle1_filtered = 0.0  # Initial filtered angle
q = 0.001  # Process noise
r = 0.01   # Measurement noise
k = 0.0    # Kalman gain

def kalman_filter(angle_measured):
    global angle1_filtered, k
    # Predict step
    angle1_predicted = angle1_filtered

    # Update step
    k = (angle1_predicted + r) / (angle1_predicted + r)  # Calculate Kalman gain
    angle1_filtered = angle1_predicted + k * (angle_measured - angle1_predicted)  # Update filtered angle

    return angle1_filtered

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

        # Calculate the angle
        angle_e = calculate_angle((shoulder_x, shoulder_y), (elbow_x, elbow_y), (wrist_x, wrist_y))
        angle_str1 = f'{int(angle_e)}'
        
        # Apply Kalman filter
        angle_filtered = kalman_filter(angle_e)
        angle_str_filtered = f'{int(angle_filtered)}'
        print(f'Filtered Angle1: {angle_str_filtered}')

        # Send only the filtered angle to Arduino
        try:
            ser.write(f"{angle_str_filtered}\n".encode())  # Send filtered angle
        except Exception as e:
            print(f"Error sending data: {e}")

        # Show the angle on the video frame
        cv2.putText(frame, angle_str_filtered, (elbow_x, elbow_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    cv2.imshow("Camera", frame)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()  # Close the serial connection when done
