import cv2
import numpy as np

hsv = None
def get_hsv_value(event, x, y, flags, param):
    global hsv
    if event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽 버튼 클릭         
        bgr_value = frame[y, x]        
        hsv_value = cv2.cvtColor(np.uint8([[bgr_value]]), cv2.COLOR_BGR2HSV)
        hsv = hsv_value[0][0]       
        print(f"클릭한 위치: ({x}, {y}) - BGR: {bgr_value} - HSV: {hsv_value[0][0]}")

points = []   #카메라 켜기 전에 만들어주기

cap = cv2.VideoCapture(0) 

while True:
    ret, frame = cap.read()

    img_hsv =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 

    if hsv is not None:
        low_hsv = np.array([hsv[0]-10, hsv[1]-10, hsv[2]-10])
        high_hsv= np.array([hsv[0]+10, hsv[1]+10, hsv[2]+10])
        mask = cv2.inRange(img_hsv, low_hsv, high_hsv)
        img_mask = cv2.bitwise_and(frame, frame, mask = mask)
        kernel = np.ones((5,5), dtype='uint8')
        img_dilate = cv2.dilate(mask, kernel = kernel, iterations=3)
        img_erod = cv2.erode(img_dilate, kernel= kernel, iterations=3)    
        img_canny = cv2.Canny(img_erod, 100, 200)
        contour, _ = cv2.findContours(img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if contour:
            c = max(contour, key = cv2.contourArea)
            img_contour = cv2.drawContours(frame, c, -1, (255, 255, 0), 3)
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 5)

        cv2.imshow('Mask', mask)
        cv2.imshow("img_dilate", img_dilate)
        cv2.imshow("img_erode", img_erod)
        cv2.imshow("img_canny", img_canny)
        cv2.imshow('img_contour', img_contour)
    
    if cv2.waitKey(10) & 0xff == ord('q'):
        break

    cv2.imshow("Frame", frame)
    cv2.setMouseCallback("Frame", get_hsv_value)  

    while True:
        c_x = c + int(w/2)
        c_y = c + int(h/2)
        points.append(c_x, c_y)
        for i in range(1, len(points)):     #p1부터 시작해야해서 1
            cv2.line(frame, (points[i-1], points[i], (0,255,255), 3))

     
   
cap.release()
cv2.destroyAllWindows()
