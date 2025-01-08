from ultralytics import YOLO
import cv2
from pymycobot.mycobot import MyCobot
import time
import os
import shutil
import numpy as np
import threading

mc = MyCobot('COM7', 115200)
time.sleep(1)
mc.set_gripper_calibration()
mc.set_gripper_mode(0)
mc.init_eletric_gripper()
time.sleep(1)
servo_speed = 30
servo_point = [[(-76.24),(-50),(-45),15.73,95.53,19.42],[-71.63, -25.83, -89.2, 23.55, 92.19, 21.18]]
servo_color_point = [[2.63,(-63.1),(-10),15.46,90.79,5], [-133, 10, -76, -2, 94, 19],[-20, -50, -10, -20, 90, 0]]

mc.send_angles([0,0,0,0,0,0],servo_speed)
time.sleep(5)
mc.send_angles(servo_point[0],servo_speed) #확인하는 위치로
time.sleep(5)

def servo_move(result_servo_point,finish_event):
    mc.send_angles([0,0,0,0,0,0],servo_speed)
    time.sleep(4)
    mc.send_angles(servo_point[1],servo_speed) #집는 위치
    time.sleep(4)
    mc.set_eletric_gripper(1)
    mc.set_gripper_value(0,20)
    time.sleep(2)
    mc.send_angles([0,0,0,0,0,0],servo_speed)
    time.sleep(5) 
    mc.send_angles(servo_color_point[result_servo_point],servo_speed) #감지된 물건 지정된 위치로
    time.sleep(4)
    mc.set_eletric_gripper(0)
    mc.set_gripper_value(100,20)
    time.sleep(2)
    mc.send_angles([0,0,0,0,0,0],servo_speed)
    time.sleep(4)
    mc.send_angles(servo_point[0],servo_speed) #다시 확인하는 위치로
    time.sleep(4)
    finish_event.set()

model = YOLO("C:/Users/eirmo/Downloads/best.pt")

cap = cv2.VideoCapture(1)
is_moving=False

while True:
    _,frame = cap.read()
    frame=cv2.flip(frame,0)
    if is_moving == False:
        results = model(frame) 

        for result in results:
            boxes = result.boxes.xyxy
            classes = result.boxes.cls
            confidences = result.boxes.conf
            names = result.names
            for box, cls, conf in zip(boxes, classes, confidences):
                name = names[int(cls)]
                if names[int(cls)]=='doraemon' or names[int(cls)]=='pooh':
                    x1, y1, x2, y2 = map(int, box)
                    cv2.putText(frame, f"{name} {conf:.2f}", (x1, y1-5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                if names[int(cls)]=='doraemon':
                    finish_event=threading.Event()
                    thread = threading.Thread(target=servo_move, args=(0,finish_event))
                    cv2.putText(frame, f"{name} {conf:.2f}", (0, 0), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)
                    is_moving=True
                    thread.start()
                if names[int(cls)]=='pooh':
                    finish_event=threading.Event()
                    thread = threading.Thread(target=servo_move, args=(2,finish_event))
                    cv2.putText(frame, f"{name} {conf:.2f}", (0, 0), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)
                    is_moving=True
                    thread.start()
    elif finish_event.is_set():
        is_moving=False
                    

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

    cv2.imshow("Detecting", frame)

cap.release()
cv2.destroyAllWindows()
                