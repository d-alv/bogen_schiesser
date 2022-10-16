import cv2 as cv
import urllib.request
import numpy as np
import math

class RunThrough():

    def __init__(self):
        """initialize variables"""
        self.url = 'http://192.168.227.194/cam-hi.jpg'
        self.max_a = 9000
        self.min_a = 100
        self.tarx = 0
        self.tary = 0
        self.c_vector = 0
        self.t_radius = 0
        self.THx = 400
        self.THy = 300
        self.arrow_mass = .0162
        self.force = 197.94
        self.l_angle = 0
        
        
    def empty(self, x):
        pass

    def setup(self):

        cv.namedWindow("trackbars")
        cv.resizeWindow("trackbars", 640, 240)
        #########################################
        cv.createTrackbar("Hue Min", "trackbars", 127,179, self.empty)
        cv.createTrackbar("Hue Max", "trackbars",171,179, self.empty)
        cv.createTrackbar("Sat Min", "trackbars",31,255, self.empty)
        cv.createTrackbar("Sat Max", "trackbars",255,255, self.empty)
        cv.createTrackbar("Val Min", "trackbars",161,255, self.empty)
        cv.createTrackbar("Val Max", "trackbars",255,255, self.empty)
        #########################################

    def runner(self):
        self.setup()
        # self.create_cross()
        while True:
            img_resp=urllib.request.urlopen(self.url)
            imgnp=np.array(bytearray(img_resp.read()), dtype=np.uint8)
            self.img=cv.imdecode(imgnp, -1)

            imgBlur = cv.GaussianBlur(self.img, (7,7), 1)

            img_hsv = cv.cvtColor(imgBlur, cv.COLOR_BGR2HSV)

            h_min = cv.getTrackbarPos("Hue Min", "trackbars")
            s_min = cv.getTrackbarPos("Sat Min", "trackbars")
            v_min = cv.getTrackbarPos("Val Min", "trackbars")
        
            h_max = cv.getTrackbarPos("Hue Max", "trackbars")
            s_max = cv.getTrackbarPos("Sat Max", "trackbars")
            v_max = cv.getTrackbarPos("Val Max", "trackbars")
        
            lower = np.array([h_min, s_min, v_min])
            upper = np.array([h_max, s_max, v_max])

            mask = cv.inRange(img_hsv, lower, upper) 
            imgresult = cv.bitwise_and(self.img, self.img, mask=mask)

            cnts, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            for c in cnts:
                area = cv.contourArea(c)
                if self.max_a >area and area>self.min_a:
                    
                    cv.drawContours(self.img, [c], -1, (255,0,0), 1)
                    M = cv.moments(c)
                    cx = int(M["m10"]/ M["m00"])
                    cy = int(M["m01"]/ M["m00"])
                    peri = cv.arcLength(c, True)
                    approx = cv.approxPolyDP(c, .02*peri, True)
                    objCor = len(approx)
                    x, y, w, h = cv.boundingRect(approx)

                    self.tarx, self.tary = (x +(w//2)), ((y)-(h//2))

                    self.c_vector = math.isqrt(int((((300-self.tary))**2)+
                                        (((400 - self.tarx))**2)))
                    self.t_radius = math.isqrt(int((abs(self.tary-(y+h))**2) + 
                                        (abs(self.tarx-(x+w))**2)))

                    # print(self.c_vector, self.t_radius)

                    hit_notif = "hit"
                    miss_notif = "miss"

                    cv.rectangle(self.img, (x,y), (x+w, y+h), (0,255,0), 1)

                    self.create_cross()

                    if objCor>=8: objectType= "circle"
                    else:
                        objectType="not_target"
                    
                    print(f"distance between = {self.c_vector-(self.t_radius-10)}")

                    if objectType == "circle":
                        if self.c_vector >= self.t_radius-10:
                            cv.putText(self.img, miss_notif, (x+(w//2)-10, y+(h//2)-10), cv.FONT_HERSHEY_COMPLEX, .5, (0,0,255), 2)
                            
                        else:
                            cv.putText(self.img, hit_notif, (x+(w//2)-10, y+(h//2)-10),cv.FONT_HERSHEY_COMPLEX, .5, (0,0,255), 2)
            
            cv.imshow("blurred", imgBlur)
            cv.imshow("HSV", img_hsv)
            cv.imshow("result", imgresult)
            cv.imshow("original", self.img)
            
            cv.waitKey(1)
    
    def create_cross(self, size=2, vposx=0, vposy=0):
        """when called, alter CH position"""
        cv.rectangle(self.img, (self.THx-1+vposx, self.THy-1+vposy),
                    (self.THx+1+vposx, self.THy+1+vposy), (255, 0, 0), size)


if __name__ == "__main__":
    RT = RunThrough()
    RT.runner()