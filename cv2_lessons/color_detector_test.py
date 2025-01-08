import numpy as np
hsv = np.load("hsv_value.npy")
print(hsv)
low_hsv = hsv[0]
high_hsv = hsv[1]

import cv2
cap = cv2.VideoCapture(0)
while True:
    _,frame = cap.read()
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

    mask = cv2.inRange(img_hsv, low_hsv, high_hsv)

    cv2.imshow("Mask", mask)

cap.release()
cv2.destroyAllWindows()