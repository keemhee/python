import cv2
import numpy as np

file = 'C:/python2/cv2_lessons/apple.webp'
img = cv2.imread(file)  

low_th_r = np.array([50, 200, 50])
high_th_r = np.array([100, 250, 100])
 
 
mask = cv2.inRange(img, low_th_r, high_th_r)
contour, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contoured_img = cv2.drawContours(img, contour, -1, (255,0,0), 3 )

cv2.imshow("apple", img)
cv2.imshow("inRange", mask)
     
cv2.waitKey(0)    

cv2.destroyAllWindows()
