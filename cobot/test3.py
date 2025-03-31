from pymycobot.mycobot import MyCobot  # MyCobot 라이브러리 임포트
import time  # 시간 지연을 위해 time 모듈 임포트
import keyboard  # 키보드 입력을 처리하기 위해 keyboard 모듈 임포트
import cv2  # OpenCV를 임포트하여 영상 처리를 수행
import os  # OS 관련 작업을 위해 os 모듈 임포트
import shutil  # 파일 복사를 위해 shutil 모듈 임포트
import numpy as np  # NumPy를 임포트하여 수치 연산을 수행

# 이미지 저장 디렉토리 설정
dir = 'images'
os.makedirs(dir, exist_ok=True)

count = 0  # 이미지 카운트 초기화

# 압축 이미지 저장 디렉토리 설정
zip_dir = 'img_zip'
os.makedirs(zip_dir, exist_ok=True)

# 웹캠에서 영상을 캡처
cap = cv2.VideoCapture(1)

# MyCobot 인스턴스 생성, 시리얼 포트와 보드레이트 설정
mc = MyCobot('COM7', 115200)
mc.send_angles([0, 0, 0, 0, 0, 0], 30)  # 초기 위치로 이동
time.sleep(2)  # 2초 대기
mc.set_gripper_mode(0)  # 그리퍼 모드 설정
mc.init_eletric_gripper()  # 전기 그리퍼 초기화
time.sleep(1)  # 1초 대기
points = []  # 각도 저장 리스트 초기화
mcspeed = 20  # 서보 모터 속도 설정

# 색상 HSV 값 설정
colors_hsv = {
    'orange': [25, 80, 100],
    'green': [135, 65, 65],
    'blue': [216, 100, 100],
    'purple': [290, 60, 50]
}

def block_to_point():
    pass

while True:
    angles = mc.get_angles()  # 각도 가져오기
    #print("각도 : ", angles)
    #time.sleep(3)

    _, frame = cap.read()  # 웹캠으로부터 프레임을 읽음
    frame = cv2.flip(frame, 0)  # 프레임을 수직으로 뒤집음

    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # 프레임을 HSV 색상 공간으로 변환
    low_hsv = np.array([colors_hsv['orange'][0] - 10, colors_hsv['orange'][1] - 10, colors_hsv['orange'][2] - 10])  # 낮은 HSV 값 설정
    high_hsv = np.array([colors_hsv['orange'][0] + 10, colors_hsv['orange'][1] + 10, colors_hsv['orange'][2] + 10])  # 높은 HSV 값 설정
    mask = cv2.inRange(img_hsv, low_hsv, high_hsv)  # 마스크 생성
    img_mask = cv2.bitwise_and(frame, frame, mask=mask)  # 마스크 적용
    kernel = np.ones((5, 5), dtype='uint8')  # 커널 생성

    key = cv2.waitKey(1) & 0xff  # 키 입력 대기

    if key == ord('q'):  # 'q' 키를 누르면 루프 종료
        break
    if key == ord('a'):  # 'a' 키를 누르면 이미지 캡처
        path = os.path.join(dir, f'img_{count}.jpg')
        cv2.imwrite(path, frame)
        print("Image captured")
        count += 1

    cv2.imshow("Detection", frame)  # 결과 프레임을 화면에 표시

    if keyboard.is_pressed('w'):  # 'w' 키를 누르면 모든 서보를 해제
        mc.release_all_servos()
        print("모든 서보를 해제합니다.")
    if keyboard.is_pressed('s'):  # 's' 키를 누르면 모든 서보를 활성화
        print("모든 서보를 활성화합니다.")
        mc.power_on()
    if keyboard.is_pressed('e'):  # 'e' 키를 누르면 각도 저장
        points.append(angles)
        print("각도 저장", angles)
    if keyboard.is_pressed('d'):  # 'd' 키를 누르면 루프 종료
        print("실행")
        break

# 확인하는 위치로 이동
mc.send_angles(points[0], mcspeed)
time.sleep(5)

# 집는 위치로 이동
mc.send_angles(points[1], mcspeed)
time.sleep(5)
mc.set_eletric_gripper(0)
mc.set_gripper_value(100, mcspeed)
time.sleep(2)
mc.set_eletric_gripper(1)
mc.set_gripper_value(0, mcspeed)
time.sleep(2)

# 오렌지 위치로 이동
mc.send_angles(points[2], mcspeed)
time.sleep(5)
mc.set_eletric_gripper(0)
mc.set_gripper_value(100, mcspeed)
time.sleep(2)
mc.set_eletric_gripper(1)
mc.set_gripper_value(0, mcspeed)
time.sleep(2)

# 그린 위치로 이동
mc.send_angles(points[3], mcspeed)
time.sleep(5)
mc.set_eletric_gripper(0)
mc.set_gripper_value(100, mcspeed)
time.sleep(2)
mc.set_eletric_gripper(1)
mc.set_gripper_value(0, mcspeed)
time.sleep(2)

# 블루 위치로 이동
mc.send_angles(points[4], mcspeed)
time.sleep(5)
mc.set_eletric_gripper(0)
mc.set_gripper_value(100, mcspeed)
time.sleep(2)
mc.set_eletric_gripper(1)
mc.set_gripper_value(0, mcspeed)
time.sleep(2)