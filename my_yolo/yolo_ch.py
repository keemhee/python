from ultralytics import YOLO  # YOLO 모델을 임포트
import cv2  # OpenCV를 임포트하여 영상 처리를 수행
from pymycobot.mycobot import MyCobot  # MyCobot 라이브러리 임포트
import time  # 시간 지연을 위해 time 모듈 임포트
import os  # OS 관련 작업을 위해 os 모듈 임포트
import shutil  # 파일 복사를 위해 shutil 모듈 임포트
import numpy as np  # NumPy를 임포트하여 수치 연산을 수행
import threading  # 멀티스레딩을 위해 threading 모듈 임포트

mc = MyCobot('COM7', 115200)  # MyCobot 인스턴스 생성, 시리얼 포트와 보드레이트 설정
time.sleep(1)  # 1초 대기
mc.set_gripper_calibration()  # 그리퍼 캘리브레이션 설정
mc.set_gripper_mode(0)  # 그리퍼 모드 설정
mc.init_eletric_gripper()  # 전기 그리퍼 초기화
time.sleep(1)  # 1초 대기
servo_speed = 30  # 서보 모터 속도 설정
servo_point = [[-76.24, -50, -45, 15.73, 95.53, 19.42], [-71.63, -25.83, -89.2, 23.55, 92.19, 21.18]]  # 서보 모터 위치 설정
servo_color_point = [[2.63, -63.1, -10, 15.46, 90.79, 5], [-133, 10, -76, -2, 94, 19], [-20, -50, -10, -20, 90, 0]]  # 색상 위치 설정

mc.send_angles([0, 0, 0, 0, 0, 0], servo_speed)  # 초기 위치로 이동
time.sleep(5)  # 5초 대기
mc.send_angles(servo_point[0], servo_speed)  # 확인하는 위치로 이동
time.sleep(5)  # 5초 대기

def servo_move(result_servo_point, finish_event):
    mc.send_angles([0, 0, 0, 0, 0, 0], servo_speed)  # 초기 위치로 이동
    time.sleep(4)  # 4초 대기
    mc.send_angles(servo_point[1], servo_speed)  # 집는 위치로 이동
    time.sleep(4)  # 4초 대기
    mc.set_eletric_gripper(1)  # 그리퍼 닫기
    mc.set_gripper_value(0, 20)  # 그리퍼 값 설정
    time.sleep(2)  # 2초 대기
    mc.send_angles([0, 0, 0, 0, 0, 0], servo_speed)  # 초기 위치로 이동
    time.sleep(5)  # 5초 대기
    mc.send_angles(servo_color_point[result_servo_point], servo_speed)  # 감지된 물건을 지정된 위치로 이동
    time.sleep(4)  # 4초 대기
    mc.set_eletric_gripper(0)  # 그리퍼 열기
    mc.set_gripper_value(100, 20)  # 그리퍼 값 설정
    time.sleep(2)  # 2초 대기
    mc.send_angles([0, 0, 0, 0, 0, 0], servo_speed)  # 초기 위치로 이동
    time.sleep(4)  # 4초 대기
    mc.send_angles(servo_point[0], servo_speed)  # 확인하는 위치로 이동
    time.sleep(4)  # 4초 대기
    finish_event.set()  # 작업 완료 이벤트 설정

model = YOLO("C:/Users/eirmo/Downloads/best.pt")  # YOLO 모델 로드

cap = cv2.VideoCapture(1)  # 웹캠에서 영상을 캡처
is_moving = False  # 로봇 팔이 움직이고 있는지 여부

while True:  # 무한 루프
    _, frame = cap.read()  # 웹캠으로부터 프레임을 읽음
    frame = cv2.flip(frame, 0)  # 프레임을 수직으로 뒤집음
    if is_moving == False:  # 로봇 팔이 움직이지 않을 때
        results = model(frame)  # 프레임에서 객체를 감지

        for result in results:  # 감지된 객체들에 대해 반복
            boxes = result.boxes.xyxy  # 바운딩 박스 좌표 가져오기
            classes = result.boxes.cls  # 객체 클래스 가져오기
            confidences = result.boxes.conf  # 객체 신뢰도 가져오기
            names = result.names  # 객체 이름 가져오기
            for box, cls, conf in zip(boxes, classes, confidences):  # 각 객체에 대해 반복
                name = names[int(cls)]  # 객체 이름 가져오기
                if names[int(cls)] == 'doraemon' or names[int(cls)] == 'pooh':  # 객체가 도라에몽 또는 푸일 경우
                    x1, y1, x2, y2 = map(int, box)  # 바운딩 박스 좌표를 정수형으로 변환
                    cv2.putText(frame, f"{name} {conf:.2f}", (x1, y1-5), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)  # 객체 이름과 신뢰도 텍스트 추가
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)  # 바운딩 박스 그리기
                if names[int(cls)] == 'doraemon':  # 객체가 도라에몽일 경우
                    finish_event = threading.Event()  # 작업 완료 이벤트 생성
                    thread = threading.Thread(target=servo_move, args=(0, finish_event))  # 서보 모터 이동 작업 스레드 생성
                    cv2.putText(frame, f"{name} {conf:.2f}", (0, 0), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)  # 객체 이름과 신뢰도 텍스트 추가
                    is_moving = True  # 로봇 팔이 움직이고 있음
                    thread.start()  # 스레드 시작
                if names[int(cls)] == 'pooh':  # 객체가 푸일 경우
                    finish_event = threading.Event()  # 작업 완료 이벤트 생성
                    thread = threading.Thread(target=servo_move, args=(2, finish_event))  # 서보 모터 이동 작업 스레드 생성
                    cv2.putText(frame, f"{name} {conf:.2f}", (0, 0), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)  # 객체 이름과 신뢰도 텍스트 추가
                    is_moving = True  # 로봇 팔이 움직이고 있음
                    thread.start()  # 스레드 시작
    elif finish_event.is_set():  # 작업 완료 이벤트가 설정되었을 경우
        is_moving = False  # 로봇 팔이 움직이지 않음

    if cv2.waitKey(5) & 0xFF == ord('q'):  # 'q' 키를 누르면 루프 종료
        break

    cv2.imshow("Detecting", frame)  # 결과 프레임을 화면에 표시

cap.release()  # 캡처 객체를 해제
cv2.destroyAllWindows()  # 모든 OpenCV 창을 닫음