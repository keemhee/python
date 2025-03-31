import numpy as np  # NumPy 라이브러리

# 저장된 HSV 값을 불러옴
hsv = np.load("hsv_value.npy")
print(hsv)

# HSV 범위 설정
low_hsv = hsv[0]
high_hsv = hsv[1]

import cv2  # OpenCV 라이브러리

# 비디오 캡처 장치 초기화 (기본 웹캠 사용)
cap = cv2.VideoCapture(0)

while True:
    # 비디오의 한 프레임을 읽음
    _, frame = cap.read()
    
    # BGR 이미지를 HSV 색 공간으로 변환
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # 'q' 키를 누르면 루프 종료
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
    
    # HSV 범위에 해당하는 마스크 생성
    mask = cv2.inRange(img_hsv, low_hsv, high_hsv)
    
    # 마스크를 윈도우에 표시
    cv2.imshow("Mask", mask)

# 비디오 캡처 해제 및 모든 창 닫기
cap.release()
cv2.destroyAllWindows()