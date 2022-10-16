import cv2 as cv
import urllib.request
import numpy as np

def nothing(x):
    pass

url='http://192.168.86.34/cam-hi.jpg'

cv.namedWindow("liv_trans", cv.WINDOW_AUTOSIZE)
cv.namedWindow("trackbars")
cv.resizeWindow("trackbars", 640, 240)


cv.createTrackbar("Hue Min", "trackbars",0,179, nothing)
cv.createTrackbar("Hue Max", "trackbars",179,179, nothing)
cv.createTrackbar("Sat Min", "trackbars",0,255, nothing)
cv.createTrackbar("Sat Max", "trackbars",255,255, nothing)
cv.createTrackbar("Val Min", "trackbars",0,255, nothing)
cv.createTrackbar("Val Max", "trackbars",255,255, nothing)

while True:
    img_resp=urllib.request.urlopen(url)
    imgnp=np.array(bytearray(img_resp.read()), dtype=np.uint8)
    frame=cv.imdecode(imgnp, -1)

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
 
    l_h = cv.getTrackbarPos("Hue Min", "trackbars")
    l_s = cv.getTrackbarPos("Sat Min", "trackbars")
    l_v = cv.getTrackbarPos("Val Min", "trackbars")
 
    u_h = cv.getTrackbarPos("Hue Max", "trackbars")
    u_s = cv.getTrackbarPos("Sat Max", "trackbars")
    u_v = cv.getTrackbarPos("Val Max", "trackbars")
 
    l_b = np.array([l_h, l_s, l_v])
    u_b = np.array([u_h, u_s, u_v])
    
    mask = cv.inRange(hsv, l_b, u_b) 
    res = cv.bitwise_and(frame, frame, mask=mask)

    cnts, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    for c in cnts:
        area=cv.contourArea(c)
        if area>2000:
            cv.drawContours(frame, [c], -1, (255, 0, 0), 3)
            M=cv.moments(c)
            cx=int(M["m10"]/M["m00"])
            cy=int(M["m01"]/M["m00"])

    cv.imshow("live transmission", frame)
    cv.imshow("mask", mask)
    cv.imshow("res", res)
    key=cv.waitKey(5)
    if key==ord('q'):
        break
    
cv.destroyAllWindows()