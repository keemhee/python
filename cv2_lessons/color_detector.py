import cv2 # opencv라이브러리
import numpy as np # numpy라이브러리

cap = cv2.VideoCapture(0) # 웹캠 영상 캡쳐

def do_nothing(value):
    pass # 트랙바 콜백함수(아무 동작도 하지 않음)

cv2.namedWindow("HSV_trackbar") #"HSV_trackbar"라는 이름의 윈도우 생성

# 트랙바 생성
cv2.createTrackbar("h_low", "HSV_trackbar", 100, 180, do_nothing)
cv2.createTrackbar("h_high", "HSV_trackbar", 100, 180, do_nothing)
cv2.createTrackbar("s_low", "HSV_trackbar", 100, 255, do_nothing)
cv2.createTrackbar("s_high", "HSV_trackbar", 100, 255, do_nothing)
cv2.createTrackbar("v_low", "HSV_trackbar", 100, 255, do_nothing)
cv2.createTrackbar("v_high", "HSV_trackbar", 100, 255, do_nothing)


while True: # 무한루프

    _ , frame = cap.read() # 웹캠으로부터 프레임 읽음
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)   #2 frame -> hsv. 프레임을 HSV 색상 공간으로 변환

    if cv2.waitKey(10) & 0xFF == ord('q'): # 'q' 누르면 루프 종료
        break

	# 트랙바의 현재 값 가져오기
    h_low = cv2.getTrackbarPos("h_low", "HSV_trackbar")
    h_high = cv2.getTrackbarPos("h_high", "HSV_trackbar")
    s_low = cv2.getTrackbarPos("s_low", "HSV_trackbar")
    s_high = cv2.getTrackbarPos("s_high", "HSV_trackbar")
    v_low = cv2.getTrackbarPos("v_low", "HSV_trackbar")
    v_high = cv2.getTrackbarPos("v_high", "HSV_trackbar")
    
    # 낮은 hsv값과 높은 hsv값을 NumPy배열로 저장
    low_hsv = np.array([h_low, s_low, v_low])             #numpy로 저장
    high_hsv = np.array([h_high, s_high, v_high])
    mask = cv2.inRange(img_hsv, low_hsv, high_hsv) # hsv값 범위에 따라 마스크 생성

    result = cv2.bitwise_and(frame, frame, mask = mask)   #컬러로 뜨게. 마스크 적용하여 결과 이미지 생성

    key = cv2.waitKey(5) & 0xFF # 키 입력 대기

    if key == ord('q'): # q누르면 루프 종료
        break
    elif key == ord('s'): # s누르면 현재 hsv값 저장
        hsv = np.array([[h_low, s_low, v_low], [h_high, s_high, v_high]])  #갖고있는 걸 리스트로 다시 만들어. low리스트 하나, high리스트 하나. 그걸 넘파이 어레이로 만들거.
        np.save("hsv_value", hsv)                                          #hsv값 잡기. 저장됨. 여기 cv2 파일에 저장될 걸..?
                                                                           #저장한 거 로드하고 싶으면 새로운 파일에서 hsv = np.load("hsv_value.npy")
                                                                                                                #  print(hsv)
                                                                                                                #  low_hsv = hsv[0]
                                                                                                                #  high_hsv = hsv[1]
                                                                                                                #  카메라 켜고
                                                                                                                #  hsv로 변경하고
                                                                                                                #  inRange()잡고
                                                                                                                #  mask 잘 보이는지 확인
                                                                                                                #  이게 잘 돼야 컨투어 딸 수 있음.
                                                                                                                #  값 가져온 게 잘 보이는지 확인. 컬러든 흑백이든
                                                                                                        
 
    #cv2.imshow("Color Detection", frame)
    cv2.imshow("HSV_trackbar", result) # 결과 이미지 표시

    cv2.imshow("Mask", mask) # 마스크 이미지 표시

cap.release() # 캡쳐 객체 해제
cv2.destroyAllWindows() # 모든 OpenCV 창 닫기