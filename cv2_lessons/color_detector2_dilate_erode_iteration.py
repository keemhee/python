import cv2
import numpy as np
cap = cv2.VideoCapture(1)
hsv = None
def get_hsv_value(event, x, y, flags, param):
    global hsv                          #밖에 있는 아이들이 변환될 때도 같이 처리됨? 여기선 클릭할 때만 발생함.
    if event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽 버튼 클릭
        bgr_value = frame[y, x]
        hsv_value = cv2.cvtColor(np.uint8([[bgr_value]]), cv2.COLOR_BGR2HSV)
        print(f"클릭한 위치: ({x}, {y}) - BGR: {bgr_value} - HSV: {hsv_value[0][0]}")
while True:
    ret, frame = cap.read()
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if hsv is not None:
        low_hsv = np.array([hsv[0]-10, hsv[1]-10, hsv[2]-10])
        high_hsv = np.array([hsv[0]+10, hsv[1]+10, hsv[2]+10])
        mask = cv2.inRange(img_hsv, low_hsv, high_hsv)
        img_mask = cv2.bitwise_and(frame, frame, mask = mask )
        kernel = np.ones((5,5), dtype='uint8')
        img_dilate = cv2.dilate(mask, kernel=kernel, iterations=3)
        img_erod = cv2.erode(img_dilate, kernel=kernel, iterations=3)
        #contour, _= cv2.findContours(img_erod, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        #img_contour = cv2.drawContours(mask, contour, -1, 100, 2)
        cv2.imshow('mask', mask)
        cv2.imshow('img_dilate', img_dilate)
        cv2.imshow('img_erode', img_erod)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    cv2.imshow('Frame', frame)
    cv2.setMouseCallback('Frame', get_hsv_value)
cap.release()
cv2.destroyAllWindows()