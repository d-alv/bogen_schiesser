from turtle import setundobuffer
import cv2 as cv
from cv2 import sqrt
import numpy as np
import math



"""" important cautionary message - this is currently tuned as if the center of the 
screen correlates to the center of the target when it shoots - this is not the case. 
This needs to be altered according to the trajectory of the arrow and the position of the camera."""

"""         TASKS TO ACCOMPLISH         """


"""         I want to set it so that it puts a dot on the screen
where the arrow will realistically land, in accordance to the drop of the arrow, and 
the pull length... maybe a quick search can help with this?

Also, configure this whole setup into class and more separate methods for if I want to
use a different camera or something. 


    INSTEAD OF USING THE MIDDLE OF THE SCREEN TO SEE IF IT MISSES, MAKE A DOT, AND USE THAT DOT'S 
    COORDINATES TO CHECK THE T_RADIUS AGAINST IT - maybe just make the "crosshair" a square, about the same right?

    make function to call when I want to shift the crosshair left or right - makes general adjustments
    rather easy
"""




def empty(x):
    pass


# def stackimages(scale, imgArray):
#     rows = len(imgArray)
#     cols = len(imgArray[0])
#     rowsAvailable = isinstance(imgArray[0], list)
#     width = imgArray[0][0].shape[1]
#     height = imgArray[0][0].shape[0]
#     if rowsAvailable:
#         for x in range(0, rows):
#             for y in range(0, cols):
#                 if imgArray[x][y].shape[:2]==imgArray[0][0].shape[:2]:


cv.namedWindow("trackbars")
cv.resizeWindow("trackbars", 640, 240)

#h_min = cv.getTrackbarPos("Hue Min", "trackbars")
#print(h_min)

def rescaleFrame(frame, scale=.2):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

#reformat = rescaleFrame(img)

cv.createTrackbar("Hue Min", "trackbars", 127,179, empty)
cv.createTrackbar("Hue Max", "trackbars",171,179, empty)
cv.createTrackbar("Sat Min", "trackbars",31,255, empty)
cv.createTrackbar("Sat Max", "trackbars",255,255, empty)
cv.createTrackbar("Val Min", "trackbars",161,255, empty)
cv.createTrackbar("Val Max", "trackbars",255,255, empty)

path = "photos/back_pic2.png"
path2 = "photos/color_bright.png"
path3 = "photos/paint.png"
while True:
    img = cv.imread(path3)
    
    imgBlur = cv.GaussianBlur(img, (7,7), 1)
    imgHSV = cv.cvtColor(imgBlur, cv.COLOR_BGR2HSV)
    

    h_min = cv.getTrackbarPos("Hue Min", "trackbars")
    h_max = cv.getTrackbarPos("Hue Max", "trackbars")
    s_min = cv.getTrackbarPos("Sat Min", "trackbars")
    s_max = cv.getTrackbarPos("Sat Max", "trackbars")
    v_min = cv.getTrackbarPos("Val Min", "trackbars")
    v_max = cv.getTrackbarPos("Val Max", "trackbars")
    #print(h_min)

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    mask = cv.inRange(imgHSV, lower, upper)
    imgresult = cv.bitwise_and(img,img,mask=mask)

    cnts, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        area = cv.contourArea(c)

        if 9000>area and area>100:
            cv.drawContours(img, [c], -1, (255,0,0), 1)
            M=cv.moments(c)
            cx = int(M["m10"]/M["m00"])
            cy=int(M["m01"]/M["m00"])
            peri = cv.arcLength(c, True)
            # print(peri)
            approx = cv.approxPolyDP(c, .02*peri, True)
            # print(len(approx)) # gives corner points
            # len gives idea of what the shape is: 8 is about circle
            objCor = len(approx)
            x, y, w, h = cv.boundingRect(approx)
            #print(x, y, w, h)
            mid_coorx, mid_coory = (x +(w//2)), ((y)-(h//2))
            # mid-point of the target (x, y)
            # print(mid_coorx, mid_coory)

            c_vector = math.isqrt(int((((300-mid_coory))**2)+
                                    (((400 - mid_coorx))**2)))

            t_radius = math.isqrt(int((abs(mid_coory-(y+h))**2) + (abs(mid_coorx-(x+w))**2)))
            print(f"distance between = {c_vector-(t_radius-10)}")

            print(mid_coory)
            print(mid_coorx)

            # print(c_vector)
            # print(t_radius)
            # print(c_vector) #vector from center of target

            # basically check if the vector from center of target 
            # to center of screen is outside bound of the target

            hit_notif = "hit"
            miss_notif = "miss"
            if c_vector >= t_radius:
                cv.putText(img, miss_notif, (x+(w//2)-10, y+(h//2)-10), cv.FONT_HERSHEY_COMPLEX, .5, 
                        (0,0,255), 2)
            else:
                cv.putText(img, hit_notif, (x+(w//2)-10, y+(h//2)-10), cv.FONT_HERSHEY_COMPLEX, .5, 
                        (0,0,255), 2)

            # dimensions of the frame 800 by 600
            cv.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 1) # this is the "targetzone"

            cv.rectangle(img, (399,299), (401, 301), (255, 0, 0), 2) # this is a "crosshair"

            cv.rectangle(img, (399,282), (401, 285), (255, 0, 0), 2)
            cv.rectangle(img, (326,137), (330, 139), (255, 0, 0), 2)
            #                   x , y     x , y         color

            # make function to call when I want to shift the crosshair left or right

            #cv.rectangle(img, (400,300), ((400 + c_vector), (300+c_vector)), (255, 0, 0), 2)
            
            # cv.rectangle(img, (600,300), (405, 390), (255, 0, 0), 2)
          
            if objCor>4: objectType="circle"
            # else:pass
            # cv.putText(img, objectType, (x+(w//2)-10, y+(h//2)-10), cv.FONT_HERSHEY_COMPLEX, .5, 
            #             (0,0,255), 2)
    cv.imshow("original", img)
    cv.imshow("HSV", imgHSV)
    cv.imshow("mask", mask)
    cv.imshow("result", imgresult)
    cv.imshow("blurry", imgBlur)
    cv.waitKey(1)
    
# cv.destroyAllWindows()


# plans - figure out how to do the object tracking stuff 
# and then overlay a crosshair onto the image that changes size 
# depending on the area of the target