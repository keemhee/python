import cv2  # OpenCV 라이브러리
import numpy as np  # NumPy 라이브러리

# 이미지 파일 경로 설정
file = 'C:/python2/cv2_lessons/apple.webp'
# 이미지 읽기
img = cv2.imread(file)  

# 빨간색 영역을 검출하기 위한 HSV 범위 설정
low_th_r = np.array([50, 200, 50])
high_th_r = np.array([100, 250, 100])

# 지정한 HSV 범위에 해당하는 마스크 생성
mask = cv2.inRange(img, low_th_r, high_th_r)

# 마스크에서 외곽선을 찾음
contour, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# 원본 이미지에 외곽선을 그림
contoured_img = cv2.drawContours(img, contour, -1, (255, 0, 0), 3)

# 결과를 화면에 표시
cv2.imshow("apple", img)
cv2.imshow("inRange", mask)

# 키 입력 대기
cv2.waitKey(0)

# 모든 창 닫기
cv2.destroyAllWindows()