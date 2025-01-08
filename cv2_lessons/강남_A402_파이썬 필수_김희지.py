import cv2
import numpy as np

def do_nothing(value):
    pass
cv2.namedWindow('Trackbar')
cv2.createTrackbar('H low', 'Trackbar', 100, 180, do_nothing)
cv2.createTrackbar('H high', 'Trackbar', 100, 180, do_nothing)
cv2.createTrackbar('S low', 'Trackbar', 150, 255, do_nothing)
cv2.createTrackbar('S high', 'Trackbar', 150, 255, do_nothing)
cv2.createTrackbar('V low', 'Trackbar', 150, 255, do_nothing)
cv2.createTrackbar('V high', 'Trackbar', 150, 255, do_nothing)
hsv = None

def get_hsv_value(val):
    h_low = cv2.getTrackbarPos('H low', 'Trackbar')
    h_high = cv2.getTrackbarPos('H high', 'Trackbar')
    s_low = cv2.getTrackbarPos('S low', 'Trackbar')
    s_high = cv2.getTrackbarPos('S high', 'Trackbar')
    v_low = cv2.getTrackbarPos('V low', 'Trackbar')
    v_high = cv2.getTrackbarPos('V high', 'Trackbar')


cap = cv2.VideoCapture(0) 

while True:
        
    ret, frame = cap.read()

    img_hsv =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if hsv is not None:
        h_low = cv2.getTrackbarPos('H low', 'Trackbar')
        h_high = cv2.getTrackbarPos('H high', 'Trackbar')
        s_low = cv2.getTrackbarPos('S low', 'Trackbar')
        s_high = cv2.getTrackbarPos('S high', 'Trackbar')
        v_low = cv2.getTrackbarPos('V low', 'Trackbar')
        v_high = cv2.getTrackbarPos('V high', 'Trackbar')
        low_hsv = np.array([h_low-10, s_low-10, v_low-10])
        high_hsv= np.array([h_high+10, s_high+10, v_high+10])
        mask = cv2.inRange(img_hsv, low_hsv, high_hsv)
        img_mask = cv2.bitwise_and(frame, frame, mask = mask)

        kernel = np.ones((5,5), dtype='uint8')

        img_dilate = cv2.dilate(mask, kernel = kernel, iterations=3)
        img_erode = cv2.erode(img_dilate, kernel= kernel, iterations=3) 
        img_canny = cv2.Canny(img_erode, 100, 200)  

        contours, _ = cv2.findContours(img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
        c = max(contours, key = cv2.contourArea)
        img_contour = cv2.drawContours(frame, c, -1, (0,0,255), 3)
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 0, 255), 5)

        cv2.imshow('Mask', mask)
        cv2.imshow("img_dilate", img_dilate)
        cv2.imshow("img_erode", img_erode)
        cv2.imshow("img_canny", img_canny)
        cv2.imshow("img_contour", img_contour)
    
    if cv2.waitKey(10) & 0xff == ord('q'):
        break


    cv2.imshow("Frame", frame)
     
   
cap.release()
cv2.destroyAllWindows()
