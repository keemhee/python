import cv2  # OpenCV 라이브러리
import numpy as np  # NumPy 라이브러리

# 마우스 클릭 이벤트를 처리하는 함수
def get_hsv_value(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽 버튼 클릭 시
        bgr_value = frame[y, x]  # 클릭한 위치의 BGR 값을 가져옴
        hsv_value = cv2.cvtColor(np.uint8([[bgr_value]]), cv2.COLOR_BGR2HSV)  # BGR 값을 HSV 값으로 변환
        print(f"클릭한 위치: ({x}, {y}) - BGR: {bgr_value} - HSV: {hsv_value[0][0]}")  # 클릭한 위치와 BGR, HSV 값을 출력

# 웹캠에서 비디오 캡처 시작
cap = cv2.VideoCapture(0) 

while True:
    ret, frame = cap.read()  # 비디오 프레임을 읽음

    if cv2.waitKey(10) & 0xff == ord('q'):  # 'q' 키를 누르면 루프 종료
        break

    cv2.imshow("Frame", frame)  # 프레임을 창에 표시
    cv2.setMouseCallback("Frame", get_hsv_value)  # 마우스 클릭 이벤트 콜백 함수 설정

# 비디오 캡처 해제 및 창 닫기
cap.release()
cv2.destroyAllWindows()

# 여기서 창 뜨면 원하는 색상 클릭해서 밑에 hsv 값 나온 거를 토대로 컬러컨투어2-2로 ㄱㄱ
# 10.10 오늘은 흰 셔츠 입어서 흰 셔츠 눌러서 HSV: [ 36   7 192] 이렇게 나옴.