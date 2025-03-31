import cv2  # OpenCV 라이브러리를 임포트

file = 'cat.jpg'  # 처리할 이미지 파일 이름
img_gray = cv2.imread(file, cv2.IMREAD_GRAYSCALE)  # 이미지를 그레이스케일로 읽기

while True:  # 무한 루프
    _, img_thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)  # 이진화 처리 (임계값 150, 최대값 255, 이진화 방법)

    cv2.imshow("Cat", img_gray)  # 원본 그레이스케일 이미지 표시
    cv2.imshow("Threshold", img_thresh)  # 이진화된 이미지 표시
    
    if cv2.waitKey(5) & 0xff == ord('q'):  # 'q' 키를 누르면 루프 종료
        break

cv2.destroyAllWindows()  # 모든 OpenCV 창 닫기
