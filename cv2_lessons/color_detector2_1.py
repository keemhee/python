import cv2
import numpy as np

def get_hsv_value(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽 버튼 클릭         
        bgr_value = frame[y, x]        
        hsv_value = cv2.cvtColor(np.uint8([[bgr_value]]), cv2.COLOR_BGR2HSV)
        print(f"클릭한 위치: ({x}, {y}) - BGR: {bgr_value} - HSV: {hsv_value[0][0]}")
 
 
cap = cv2.VideoCapture(0) 

while True:
    ret, frame = cap.read()

    if cv2.waitKey(10) & 0xff == ord('q'):
        break

    cv2.imshow("Frame", frame)
    cv2.setMouseCallback("Frame", get_hsv_value)
     
   
cap.release()
cv2.destroyAllWindows()

#여기서 창 뜨면 원하는 색상 클릭해서 밑에 hsv 값 나온 거를 토대로 컬러컨투어2-2로 ㄱㄱ
#10.10 오늘은 흰 셔츠 입어서 흰 셔츠 눌러서 HSV: [ 36   7 192] 이렇게 나옴.