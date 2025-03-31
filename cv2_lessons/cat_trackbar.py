import cv2  # OpenCV 라이브러리를 임포트

file = 'cat.jpg'  # 처리할 이미지 파일 이름
img_gray = cv2.imread(file, cv2.IMREAD_GRAYSCALE)  # 이미지를 그레이스케일로 읽기

def do_nothing(value):
    pass  # 트랙바 콜백 함수 (아무 동작도 하지 않음)

cv2.namedWindow("Trackbar")  # "Trackbar"라는 이름의 윈도우 생성
cv2.createTrackbar("threshold", "Trackbar", 100, 255, do_nothing)  # 트랙바 생성 (이름: "threshold", 초기값: 100, 최대값: 255, 콜백 함수: do_nothing)

while True:  # 무한 루프
    thresh_value = cv2.getTrackbarPos("threshold", "Trackbar")  # 트랙바의 현재 값 가져오기
    _, img_thresh = cv2.threshold(img_gray, thresh_value, 255, cv2.THRESH_BINARY)  # 이진화 처리 (임계값: 트랙바 값, 최대값: 255, 이진화 방법)

    cv2.imshow("Cat", img_gray)  # 원본 그레이스케일 이미지 표시
    cv2.imshow("Threshold", img_thresh)  # 이진화된 이미지 표시
    
    if cv2.waitKey(5) & 0xff == ord('q'):  # 'q' 키를 누르면 루프 종료
        break

cv2.destroyAllWindows()  # 모든 OpenCV 창 닫기