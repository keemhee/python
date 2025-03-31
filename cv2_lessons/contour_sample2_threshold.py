import cv2  # OpenCV 라이브러리

# 이미지 파일 경로 설정
file = 'C:/python2/cv2_lessons/number1.png'

# 이미지를 읽어옴
img = cv2.imread(file)

# 이미지를 그레이스케일로 변환
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 이진화 처리 (임계값: 200)
_, thresh_img = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY_INV)

# 이진화된 이미지에서 외곽선 찾기
contour, _ = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 가장 큰 외곽선 선택
c = max(contour, key=cv2.contourArea)

# 외곽선의 경계 사각형 계산
x, y, w, h = cv2.boundingRect(c)
print(x, y, w, h)  # 경계 사각형의 좌표와 크기 출력

# 원본 이미지에 외곽선을 그림
contour_img = cv2.drawContours(img, contour, -1, (255, 255, 0), 5)

# 결과 이미지들을 화면에 표시
cv2.imshow("Original", thresh_img)
cv2.imshow("Contoured", contour_img)

# 키 입력 대기
cv2.waitKey(0)

# 모든 창 닫기
cv2.destroyAllWindows()