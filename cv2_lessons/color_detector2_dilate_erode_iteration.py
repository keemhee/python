import cv2  # OpenCV 라이브러리
import numpy as np  # NumPy 라이브러리

# 비디오 캡처 장치 인덱스를 1로 설정 (0으로 변경하면 기본 웹캠 사용 가능)
cap = cv2.VideoCapture(1)
hsv = None  # 전역 변수 hsv 초기화

# 마우스 클릭 이벤트를 처리하는 함수
def get_hsv_value(event, x, y, flags, param):
    global hsv  # 전역 변수 hsv 사용
    if event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽 버튼 클릭 시
        bgr_value = frame[y, x]  # 클릭한 위치의 BGR 값을 가져옴
        hsv_value = cv2.cvtColor(np.uint8([[bgr_value]]), cv2.COLOR_BGR2HSV)  # BGR 값을 HSV 값으로 변환
        hsv = hsv_value[0][0]  # 전역 변수 hsv에 HSV 값을 설정
        print(f"클릭한 위치: ({x}, {y}) - BGR: {bgr_value} - HSV: {hsv}")  # 클릭한 위치와 BGR, HSV 값을 출력

while True:
    ret, frame = cap.read()  # 비디오 프레임을 읽음
    if not ret:  # 프레임 읽기 실패 시 루프 종료
        break

    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # 현재 프레임을 HSV 색 공간으로 변환
    if hsv is not None:  # hsv 값이 설정된 경우
        # HSV 값의 범위를 설정하여 마스크 생성
        low_hsv = np.array([hsv[0] - 10, hsv[1] - 10, hsv[2] - 10])
        high_hsv = np.array([hsv[0] + 10, hsv[1] + 10, hsv[2] + 10])
        mask = cv2.inRange(img_hsv, low_hsv, high_hsv)  # 지정한 HSV 범위에 해당하는 마스크 생성
        img_mask = cv2.bitwise_and(frame, frame, mask=mask)  # 원본 이미지와 마스크를 AND 연산
        
        # 커널 생성 및 침식과 팽창 연산
        kernel = np.ones((5, 5), dtype='uint8')
        img_dilate = cv2.dilate(mask, kernel=kernel, iterations=3)  # 팽창 연산
        img_erod = cv2.erode(img_dilate, kernel=kernel, iterations=3)  # 침식 연산
        
        # 결과 이미지들을 윈도우에 표시
        cv2.imshow('mask', mask)
        cv2.imshow('img_dilate', img_dilate)
        cv2.imshow('img_erode', img_erod)

    if cv2.waitKey(10) & 0xFF == ord('q'):  # 'q' 키를 누르면 루프 종료
        break

    cv2.imshow('Frame', frame)  # 원본 프레임을 윈도우에 표시
    cv2.setMouseCallback('Frame', get_hsv_value)  # 마우스 클릭 이벤트 콜백 함수 설정

cap.release()  # 비디오 캡처 해제
cv2.destroyAllWindows()  # 모든 창 닫기