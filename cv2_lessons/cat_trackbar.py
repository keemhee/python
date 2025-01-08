import cv2

file = 'cat.jpg'
img_gray = cv2.imread(file, cv2.IMREAD_GRAYSCALE) 

def do_nothing(value):
    pass

cv2.namedWindow("Trackbar")
cv2.createTrackbar("threshold", "Trackbar", 100, 255, do_nothing)

while True: 

    thresh_value = cv2.getTrackbarPos("threshold", "Trackbar")
    _, img_thresh =cv2.threshold(img_gray, thresh_value, 255, cv2.THRESH_BINARY) 

    cv2.imshow("Cat", img_gray)
    cv2.imshow("Threshold", img_thresh)
    
    if cv2.waitKey(5) & 0xff == ord('q'):
        break      

cv2.destroyAllWindows()