import cv2
import numpy as np

cap = cv2.VideoCapture(0)    #

def do_nothing(value):
    pass

cv2.namedWindow("HSV_trackbar")

cv2.createTrackbar("h_low", "HSV_trackbar", 100, 180, do_nothing)
cv2.createTrackbar("h_high", "HSV_trackbar", 100, 180, do_nothing)
cv2.createTrackbar("s_low", "HSV_trackbar", 100, 255, do_nothing)
cv2.createTrackbar("s_high", "HSV_trackbar", 100, 255, do_nothing)
cv2.createTrackbar("v_low", "HSV_trackbar", 100, 255, do_nothing)
cv2.createTrackbar("v_high", "HSV_trackbar", 100, 255, do_nothing)


while True:

    _ , frame = cap.read()
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)   #2 frame -> hsv

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break


    h_low = cv2.getTrackbarPos("h_low", "HSV_trackbar")
    h_high = cv2.getTrackbarPos("h_high", "HSV_trackbar")
    s_low = cv2.getTrackbarPos("s_low", "HSV_trackbar")
    s_high = cv2.getTrackbarPos("s_high", "HSV_trackbar")
    v_low = cv2.getTrackbarPos("v_low", "HSV_trackbar")
    v_high = cv2.getTrackbarPos("v_high", "HSV_trackbar")
    low_hsv = np.array([h_low, s_low, v_low])             #numpy로 저장
    high_hsv = np.array([h_high, s_high, v_high])
    mask = cv2.inRange(img_hsv, low_hsv, high_hsv)

    result = cv2.bitwise_and(frame, frame, mask = mask)   #컬러로 뜨게

    key = cv2.waitKey(5) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('s'):
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
    cv2.imshow("HSV_trackbar", result)

    cv2.imshow("Mask", mask)

cap.release()
cv2.destroyAllWindows()