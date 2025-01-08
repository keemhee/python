'''
파이썬으로 블록 움직이기(블록코딩 변경)
새로운 포인트 추가(release_all())
3포인트를 변수로 만들기
카메라 연결
cnn모델_양품과 불량 분류 처리'''

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

# os.path.join(dir, f'image_{count}.jpg')
cap = cv2.VideoCapture(1)

mc = MyCobot('COM7', 115200)
mc.send_angles([0, 0, 0, 0, 0, 0], 30)
time.sleep(2)
mc.set_gripper_mode(0)
mc.init_eletric_gripper()
time.sleep(1)
points=[]

while True:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
    angles = mc.get_angles()
    #print("각도 : ", angles)
    #time.sleep(3)

    _, frame = cap.read()
    frame = cv2.flip(frame, 0)
   
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



mc.send_angles([0, 0, 0, 0, 0, 0], 30)
time.sleep(5)
print("물건 스캔")
mc.send_angles(points[0], 20)
time.sleep(5)
mc.set_eletric_gripper(0)
mc.set_gripper_value(100, 20)
time.sleep(2)
mc.set_eletric_gripper(1)
mc.set_gripper_value(0, 20)
time.sleep(2)
mc.send_angles([0, 0, 0, 0, 0, 0], 30)
time.sleep(5)

if
print("양품입니다")
mc.send_angles(points[1], 20)
time.sleep(5)
mc.set_eletric_gripper(0)
mc.set_gripper_value(100, 20)
time.sleep(2)
mc.send_angles([0, 0, 0, 0, 0, 0], 30)
time.sleep(5)

if
print("불량입니다")
mc.send_angles(points[2], 20)
time.sleep(5)
mc.set_eletric_gripper(0)
mc.set_gripper_value(100, 20)
time.sleep(2)
mc.send_angles([0, 0, 0, 0, 0, 0], 30)
time.sleep(5)

cap.release()
cv2.destroyAllWindows()

zip_dir_path = os.path.join(zip_dir, 'archive')
shutil.make_archive(zip_dir_path , 'zip', dir)

import cv2
import numpy as np

hsv = None
def get_hsv_value(event, x, y, flags, param):
    global hsv
    if event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽 버튼 클릭         
        bgr_value = frame[y, x]        
        hsv_value = cv2.cvtColor(np.uint8([[bgr_value]]), cv2.COLOR_BGR2HSV)
        hsv = hsv_value[0][0]       
        print(f"클릭한 위치: ({x}, {y}) - BGR: {bgr_value} - HSV: {hsv_value[0][0]}")

cap = cv2.VideoCapture(0) 

while True:
    ret, frame = cap.read()

    img_hsv =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 

    if hsv is not None:
        low_hsv = np.array([hsv[0]-10, hsv[1]-10, hsv[2]-10])
        high_hsv= np.array([hsv[0]+10, hsv[1]+10, hsv[2]+10])
        mask = cv2.inRange(img_hsv, low_hsv, high_hsv)
        img_mask = cv2.bitwise_and(frame, frame, mask = mask)
        kernel = np.ones((5,5), dtype='uint8')
        img_dilate = cv2.dilate(mask, kernel = kernel, iterations=3)
        img_erod = cv2.erode(img_dilate, kernel= kernel, iterations=3)    
        img_canny = cv2.Canny(img_erod, 100, 200)


        contour, _ = cv2.findContours(img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        c = max(contour, key = cv2.contourArea)
        img_contour = cv2.drawContours(frame, c, -1, (255, 255, 0), 3)
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 5)

        cv2.imshow('Mask', mask)
        cv2.imshow("img_dilate", img_dilate)
        cv2.imshow("img_erode", img_erod)
        cv2.imshow("img_canny", img_canny)
        cv2.imshow('img_contour', img_contour)
    
    if cv2.waitKey(10) & 0xff == ord('q'):
        break

    cv2.imshow("Frame", frame)
    cv2.setMouseCallback("Frame", get_hsv_value)  
     
   
cap.release()
cv2.destroyAllWindows()
