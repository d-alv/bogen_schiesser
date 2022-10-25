""" pay attention to 91 and 92"""

import cv2 as cv
import urllib.request
import numpy as np
import math
from physics import PH
from angle import Angle

class RunThrough():

    def __init__(self):
        """initialize variables"""
        self.url = 'http://192.168.169.194/cam-hi.jpg'
        self.x =0 #iterator
        self.max_a = 9000
        self.min_a = 100
        self.tarx = 0
        self.tary = 0
        self.c_vector = 0
        self.t_radius = 0
        self.THx = 400
        self.THy = 300
        self.dist_angle = 1.051650213
        self.PH = PH()
        self.distance = 0
        self.real_ang = 1.5211059
        self.Angle = Angle()

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
        frame = cv.VideoCapture(0)
        frame_width = 800
        frame_height = 600
        frame.set(3, frame_width)
        frame.set(4, frame_height)


        # self.create_cross()
        while True:

            ret, self.img = frame.read()
            if ret == False:
                print("not getting signal from camera!")
                break
            print(self.Angle.analog_read()) #continuously gets the angle :)

            # img_resp=urllib.request.urlopen(self.url)
            # imgnp=np.array(bytearray(img_resp.read()), dtype=np.uint8)
            # self.img=cv.imdecode(imgnp, -1)

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

                    self.calc_distance(width=w)

                    self.tarx, self.tary = (x +(w//2)), ((y)-(h//2))

                    self.c_vector = math.isqrt(int((((300-self.tary))**2)+
                                        (((400 - self.tarx))**2))) #measures in accordance to 
                                        # center of screen ^^^^^
                    self.t_radius = math.isqrt(int((abs(self.tary-((y+h)//4)**2) + 
                                        (abs(self.tarx-((x+w)//4))**2))))
                                

                    # print(self.c_vector, self.t_radius)

                    hit_notif = "hit"
                    miss_notif = "miss"

                    cv.rectangle(self.img, (x,y), (x+w, y+h), (0,255,0), 1)

                    ############################# create precision box
                    cv.rectangle(self.img, (int(x+(w*.25)),int(y+(h*.25))), 
                                (int(x+(w*.75)), int(y+(h*.75))), (0, 0, 255), 1)

                    self.calc_distance(width=w)
                    # self.calc_arrow_drop(y_val=h)
                    #print(self.calc_arrow_drop(y_val=h))
                    #
                    self.create_cross(drop=self.calc_arrow_drop(y_val=h))

                    if objCor>=8: objectType= "circle"
                    else:
                        objectType="not_target"
                    
                    #print(f"distance between = {self.c_vector-(self.t_radius-10)}")

                    if objectType == "circle":
                        if self.c_vector >= self.t_radius:
                            cv.putText(self.img, miss_notif, (x+(w//2)-10, y+(h//2)-10), cv.FONT_HERSHEY_COMPLEX, .5, (0,0,255), 2)
                            
                        else:
                            cv.putText(self.img, hit_notif, (x+(w//2)-10, y+(h//2)-10),cv.FONT_HERSHEY_COMPLEX, .5, (0,0,255), 2)
            
            cv.imshow("blurred", imgBlur)
            cv.imshow("HSV", img_hsv)
            cv.imshow("result", imgresult)
            cv.imshow("original", self.img)
            
            cv.waitKey(1)
    
    def create_cross(self, size=2, vposx=0, vposy=0, drop=0): #drop uses physics to see how much lower it'll be
        """when called, alter CH position; first box is where bow aiming,
            second is arrow's expected hit point"""
        cv.rectangle(self.img, (self.THx-1+vposx, self.THy-1+vposy),
                    (self.THx+1+vposx, self.THy+1+vposy), (255, 0, 0), size)

        cv.rectangle(self.img, (self.THx-1+vposx, self.THy-1+vposy+drop),
                    (self.THx+1+vposx, self.THy+1+vposy+drop), (0, 255, 0), size)

    def calc_distance(self, width):
        self.distance = math.tan(width/self.dist_angle)
        self.x+=1
        
        if self.distance<0:
            self.distance=0
        if self.x==5:
            print(f"currently at distance {self.distance}")
            self.x=0

        

    def calc_arrow_drop(self, y_val): #y_val is the y distance value for target: h 
        """grabs the angle and the velocity to find how far the 
        arrow will fall from the distance to the target
        
        lots of conversion between feet and pixels"""

        #grab the angle from the other program
        t_t_h = self.distance/self.PH.calc_speed() #stands for time to hit // I don't think this works
        upward_vel = self.PH.calc_speed()*math.sin(abs(self.Angle.rad))
        if self.Angle.rad >0:
            pass
        elif self.Angle.rad<0:
            upward_vel = -1*upward_vel

        dist_lower =  (t_t_h*upward_vel) + (.5*(-9.81)*(t_t_h**2))

        # dist_lower value is negative, meaning just add it to the other stuff


        #convert actual distance to pixels on screen, based on how far away I'm standing. 

        # GO HOME && MEASURE THE X AND Y AXIS OF TARGET (PINK PART) AND COMPARE THAT 
        # at the 11 meters it should mean .2921 meters is 17 pxls or whatever
        y = math.tan(self.real_ang)*self.dist_angle

        # not sure how this works ^ check later

        pixels_down = (y_val*dist_lower)/y
        return(int(pixels_down))

if __name__ == "__main__":
    RT = RunThrough()
    RT.runner()