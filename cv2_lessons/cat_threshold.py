import cv2

file = 'cat.jpg'
img_gray = cv2.imread(file, cv2.IMREAD_GRAYSCALE) 

while True: 
    _, img_thresh =cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY) 

    cv2.imshow("Cat", img_gray)
    cv2.imshow("Threshold", img_thresh)
    
    if cv2.waitKey(5) & 0xff == ord('q'):
        break      

cv2.destroyAllWindows()