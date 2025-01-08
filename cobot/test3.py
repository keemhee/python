from pymycobot.mycobot import MyCobot
import time
import keyboard
import cv2 
import os
import shutil
from tensorflow.keras.models import load_model
import numpy as np

dir = 'images'
os.makedirs(dir, exist_ok=True)

count = 0

zip_dir = 'img_zip'
os.makedirs(zip_dir, exist_ok= True)

cap = cv2.VideoCapture(1)

mc = MyCobot('COM7', 115200)
mc.send_angles([0, 0, 0, 0, 0, 0], 30)
time.sleep(2)
mc.set_gripper_mode(0)
mc.init_eletric_gripper()
time.sleep(1)
points=[]
mcspeed = 20

colors_hsv = {'orange':[25, 80, 100], 
       'green':[135, 65, 65],
       'blue':[216, 100, 100],
       'purple':[290, 60, 50]}

def block_to_point():
    pass

while True:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
    angles = mc.get_angles()
    #print("각도 : ", angles)
    #time.sleep(3)

    _, frame = cap.read()
    frame = cv2.flip(frame, 0)

    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    low_hsv = np.array([colors_hsv[0]-10, colors_hsv[1]-10, colors_hsv[2]-10])
    high_hsv = np.array([colors_hsv[0]+10, colors_hsv[1]+10, colors_hsv[2]+10])
    mask = cv2.inRange(img_hsv, low_hsv, high_hsv)
    img_mask = cv2.bitwise_and(frame, frame, mask = mask )
    kernel = np.ones((5,5), dtype='uint8')
   
    key = cv2.waitKey(1) & 0xff 

    if key == ord('q'):
        break
    if key == ord('a'):
        path = os.path.join(dir, f'img_{count}.jpg') 
        cv2.imwrite(path , frame)
        print("Image captured")
        count += 1

    cv2.imshow("Detection", frame)

    if keyboard.is_pressed('w'):
        mc.release_all_servos()
        print("모든 서보를 해제합니다.")
    if keyboard.is_pressed('s'):
        print("모든 서보를 활성화합니다.")
        mc.power_on()
    if keyboard.is_pressed('e'):
        points.append(angles)
        print("각도 저장", angles)
    if keyboard.is_pressed('d'):
        print("실행")
        break

#확인하는 위치
mc.send_angles(points[0], mcspeed)
time.sleep(5)

#집는 위치
mc.send_angles(points[1], mcspeed)
time.sleep(5)
mc.set_eletric_gripper(0)
mc.set_gripper_value(100, mcspeed)
time.sleep(2)
mc.set_eletric_gripper(1)
mc.set_gripper_value(0, mcspeed)
time.sleep(2)

#오렌지
mc.send_angles(points[2], mcspeed)
time.sleep(5)
mc.set_eletric_gripper(0)
mc.set_gripper_value(100, mcspeed)
time.sleep(2)
mc.set_eletric_gripper(1)
mc.set_gripper_value(0, mcspeed)
time.sleep(2)

#그린
mc.send_angles(points[3], mcspeed)
time.sleep(5)
mc.set_eletric_gripper(0)
mc.set_gripper_value(100, mcspeed)
time.sleep(2)
mc.set_eletric_gripper(1)
mc.set_gripper_value(0, mcspeed)
time.sleep(2)

#블루
mc.send_angles(points[4], mcspeed)
time.sleep(5)
mc.set_eletric_gripper(0)
mc.set_gripper_value(100, mcspeed)
time.sleep(2)
mc.set_eletric_gripper(1)
mc.set_gripper_value(0, mcspeed)
time.sleep(2)