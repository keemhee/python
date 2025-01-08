import mediapipe as mp
import cv2
import numpy as np

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

        cv2.circle(frame, (shoulder_x, shoulder_y), 3, (255, 0, 0), -1)
        cv2.circle(frame, (elbow_x, elbow_y), 3, (255, 0, 0), -1)
        cv2.circle(frame, (wrist_x, wrist_y), 3, (255, 0, 0), -1)
        cv2.circle(frame, (thumb_x, thumb_y), 3, (255, 0, 0), -1)
        cv2.line(frame, (shoulder_x, shoulder_y), (elbow_x, elbow_y), (0, 255, 0), 2)
        cv2.line(frame, (elbow_x, elbow_y), (wrist_x, wrist_y), (0, 255, 0), 2)
        cv2.line(frame, (wrist_x, wrist_y), (thumb_x, thumb_y), (0, 255, 0), 2)

        angle_e = calculate_angle((shoulder_x, shoulder_y), (elbow_x, elbow_y), (wrist_x, wrist_y))
        angle_str1 = f'{int(angle_e)}'
        print(f'angle1: {angle_str1}')
        cv2.putText(frame, angle_str1, (elbow_x, elbow_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        '''
        angle_w = calculate_angle((elbow_x, elbow_y), (wrist_x, wrist_y), (thumb_x, thumb_y))
        angle_str2 = f'{int(angle_w)}'
        print(f'angle2: {angle_str2}')
        cv2.putText(frame, angle_str2, (wrist_x, wrist_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        '''
        
    except Exception as e:
        print("어깨가 보이지 않습니다.")

    cv2.imshow("Motion Tracking", frame)    
        
    if cv2.waitKey(5) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()