import cv2

file = 'C:/python2/cv2_lessons/number1.png'

img = cv2.imread(file)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, thresh_img = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY_INV)

contour, _ = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
c = max(contour, key = cv2.contourArea)

x, y, w, h = cv2.boundingRect(c)
print(x, y, w, h)

contour_img = cv2.drawContours(img, contour, -1, (255,255,0), 5)
##  숫자에 사각형 표시하기

cv2.imshow("Original", thresh_img)
cv2.imshow("Contoured", contour_img)


cv2.waitKey(0)

cv2.destroyAllWindows()