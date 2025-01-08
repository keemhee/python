import cv2
import numpy as np

def get_hsv_value(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽 버튼 클릭         
        bgr_value = frame[y, x]        
        hsv_value = cv2.cvtColor(np.uint8([[bgr_value]]), cv2.COLOR_BGR2HSV)
        print(f"클릭한 위치: ({x}, {y}) - BGR: {bgr_value} - HSV: {hsv_value[0][0]}")
 
low_hsv = np.array([130, 35, 120])
high_hsv = np.array([160, 60, 150])
 
cap = cv2.VideoCapture(0) 

while True:
    ret, frame = cap.read()      #비디오의 한 프레임씩 읽어줌. ret는 결과를 말함.

    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(img_hsv, low_hsv, high_hsv)
    img_mask = cv2.bitwise_and(frame, frame, mask = mask)
    kernel = np.ones((5, 5), dtype = 'uint8')

    img_dilate = cv2.dilate(mask, kernel = kernel)    #이미지 컬러를 확장해주는 역할. 더 진하게? 노이즈도 확장됨
    #img_erod = cv2.erode(mask, kernel = kernel)      #노이즈 지우는 거. 
    img_erod = cv2.erode(img_dilate, kernel = kernel) # dilate한 거를 가지고 erode하면 노이즈가 좀 더 지워졌는지 볼 수 있음. 여기 원본 mask보다 매끄러워짐.
    img_canny = cv2.Canny(img_erod, 100, 200)

    contour, _ = cv2.findContours(img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contour, key = cv2.contourArea)
    img_contour = cv2.drawContours(frame, c, -1, (255, 255, 0), 3)
    
    if cv2.waitKey(10) & 0xff == ord('q'):
        break

    cv2.drawContours(frame, c, -1, (255, 255, 0), 3)
    #cv2.imshow("Frame", frame)
    cv2.setMouseCallback("Frame", get_hsv_value)
    cv2.imshow("Mask", mask)
    cv2.imshow("img_dilate", img_dilate)
    cv2.imshow("img_erode", img_erod)
    cv2.imshow("img_canny", img_canny)
    cv2.imshow("img_contour", img_contour)

cap.release()
cv2.destroyAllWindows()
