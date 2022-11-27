import cv2 as cv
import urllib.request
import numpy as np
import math
from physics import PH
from angle import Angle
from buzz import Buzzing
import time
from picamera.array import PiRGBArray
from picamera import PiCamera

#camera = PiCamera()

class RunThrough():

    def __init__(self):
        """initialize variables"""
        self.x =0 #iterator
        self.set=False # checks if on targ already
        self.g = 0 # helps stop buzzer
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
        self.Buzzing=Buzzing()
        self.camera=PiCamera()
        self.cb = [[],[]]
        self.ct=[] #color test
        self.hor_fov = .93375
        self.hor_rem=1.1039 # 2pi - hor_fov / 2
        self.ver_fov = .72274
        self.ver_rem = 1.2094
        self.ratio=0
        self.THdrop = 0
        


    def empty(self, x):
        pass

    def setup(self):
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = 1.0
        self.camera.exposure_mode='sports'
        #self.camera.iso=800
        self.camera.rotation = 270 # 0, 90, 180, and 270 accepted


        #cv.namedWindow("trackbars", cv.WINDOW_NORMAL)
        #cv.resizeWindow("trackbars", 240, 240)
        #########################################
        #cv.createTrackbar("Hue Min", "trackbars", 149,179, self.empty)
        #cv.createTrackbar("Hue Max", "trackbars",168,179, self.empty)
        #cv.createTrackbar("Sat Min", "trackbars",85,255, self.empty)
        #cv.createTrackbar("Sat Max", "trackbars",239,255, self.empty)
        #cv.createTrackbar("Val Min", "trackbars",107,255, self.empty)
        #cv.createTrackbar("Val Max", "trackbars",255,255, self.empty)
        #########################################
        
        
        # IF NEED CHANGE COLOR CONFIGS, LOOK UP HERE ^^^


    def runner(self):
        #cv.startWindowThread()
        self.setup()
        
        self.camera.resolution = (800, 600)
        self.camera.framerate=60
        rawCapture = PiRGBArray(self.camera, size=(800,600))

        time.sleep(.1)

        # self.create_cross()
        while True:
            
            for frame in self.camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                self.img = frame.array
                self.g+=1

                imgBlur = cv.GaussianBlur(self.img, (7,7), 1)
                #print("after blur")
                img_hsv = cv.cvtColor(imgBlur, cv.COLOR_BGR2HSV)

                #self.ct[0] = cv.getTrackbarPos("Hue Min", "trackbars")
                #self.ct[1] = cv.getTrackbarPos("Sat Min", "trackbars")
                #self.ct[2] = cv.getTrackbarPos("Val Min", "trackbars")
            
                #self.ct[3] = cv.getTrackbarPos("Hue Max", "trackbars")
                #self.ct[4] = cv.getTrackbarPos("Sat Max", "trackbars")
                #self.ct[5] = cv.getTrackbarPos("Val Max", "trackbars")
                
                self.get_masks(img_hsv)
                #cv.rectangle(self.img, (self.THx-1, self.THy-1),
                 #   (self.THx+1, self.THy+1), (255, 0, 0), 2)
                # REMEMBER TO DELETE THIS:: TEST ONLY

                if self.g != self.Buzzing.x:self.Buzzing.no_targ()

                #cv.imshow("result", imgresult)
                #cv.imshow("HSV", img_hsv)
                #cv.imshow("Frame", self.img)
                key=cv.waitKey(1) & 0xFF
                rawCapture.truncate(0)

    def get_masks(self, img_hsv):

        colors = [[0, 0, 134, 179, 32, 255],
        [57, 154, 159, 164, 256, 253]] #first is white, second is red

        ID = 0
        for color in colors:
            ID +=1 # white has ID 1, red has ID 2
            lower = np.array([color[0:3]])
            upper = np.array([color[3:6]])
            mask = cv.inRange(img_hsv, lower, upper)
            imgresult = cv.bitwise_and(self.img, self.img, mask=mask)
            self.get_contour(mask, ID)

    def get_contour(self, mask, ID):
        """possible problem: might be too slow of a process"""
        
        targ_dict={}
        cnts, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        if ID==1: self.max_a, self.min_a = 5000, 500
        else: self.max_a, self.min_a = 10000, 100
        for c in cnts:
            area = cv.contourArea(c)
            if self.max_a >area and area>self.min_a:
                #figure out how many qualify and are here
                
                        
                cv.drawContours(self.img, [c], -1, (255,0,0), 1)
                M = cv.moments(c)
                cx = int(M["m10"]/ M["m00"]) #if other doesn't work, try this centroid relation
                cy = int(M["m01"]/ M["m00"])
                peri = cv.arcLength(c, True)
                approx = cv.approxPolyDP(c, .02*peri, True)
                objCor = len(approx)
                x, y, w, h = cv.boundingRect(approx)
                self.cb[ID-1]= [x, y, x+w, y+h]
                
                
                if ID == 2:
                    if cx > self.cb[0][0] and cx< self.cb[0][2]:
                        if cy > self.cb[0][1] and cy< self.cb[0][3]:
                            self.get_rectangles(x,y,w,h)

                else:
                    
                    print(objCor)
                    net_distance = int(math.sqrt(((self.THy - cy )**2) + ((self.THx - cx)**2)))
                    targ_dict[net_distance]=[x,y,w,h]
                    
        if not targ_dict.keys():
            pass
        else:
            v = targ_dict[min(targ_dict.keys())]
            self.get_rectangles(v[0],v[1],v[2],v[3])
            self.pos_calculations(v[0],v[1],v[2],v[3])
        
                    
    

    def pos_calculations(self, x,y,w,h):
        """calculates distance/ if hit or miss/"""
        self.calc_distance(w=w, h=h)
        self.create_cross(drop=self.calc_arrow_drop(h))
        self.tarx, self.tary = (x +(w//2)), (y-(h//2)) #get center of target

        if self.THx >= int(x+(w*.25)) and self.THx <= x+int((w*.75)):
            c_xcheck=True
        else:
            c_xcheck=False
        if self.THdrop >= int(y+(h*.25)) and self.THdrop <= y+(h*.75):
            c_ycheck=True
        else:c_ycheck=False
        net_distance = int(math.sqrt(((self.THy - self.tary )**2) + ((self.THx - self.tarx)**2)))
        
        self.g = self.Buzzing.x+1
        if c_xcheck and c_ycheck:
                                
            cv.putText(self.img, "hit", (x+(w//2)-10, y+(h//2)-10),cv.FONT_HERSHEY_COMPLEX, .5, (0,0,255), 2)
            #if self.set==False:
            self.Buzzing.buzz_now(net_distance,True)
                #self.set=True
                            
        else:
            #self.set=False
                                
            self.Buzzing.buzz_now(net_distance)
            cv.putText(self.img, "miss", (x+(w//2)-10, y+(h//2)-10), cv.FONT_HERSHEY_COMPLEX, .5, (0,0,255), 2)
    
    def get_rectangles(self, x, y, w, h):
        cv.rectangle(self.img, (x,y), (x+w, y+h), (0,255,0), 1)

        ############################# create precision box
        cv.rectangle(self.img, (int(x+(w*.25)),int(y+(h*.25))), 
        (int(x+(w*.75)), int(y+(h*.75))), (0, 0, 255), 1)

    
    def create_cross(self, size=2, vposx=0, vposy=0, drop=0): #drop uses physics to see how much lower it'll be
        """when called, alter CH position; first box is where bow aiming,
            second is arrow's expected hit point"""
        cv.rectangle(self.img, (self.THx-1+vposx, self.THy-1+vposy),
                    (self.THx+1+vposx, self.THy+1+vposy), (255, 0, 0), size)

        cv.rectangle(self.img, (self.THx-1+vposx, self.THy-1+vposy-drop),
                    (self.THx+1+vposx, self.THy+1+vposy-drop), (0, 255, 0), size)
        self.THdrop = self.THy-drop
        print(f"drop is: {drop}")


    def calc_distance(self, w, h):

        print(f"w is {w}")
        tar_size=.508 # meters
        total_x = (800/w)*tar_size
        print("total x")
        print(total_x)
        total_y = (600//h)*tar_size # fits 20 times, adjust this for what a distance of 20 is
        self.ratio=h/tar_size
        z_h=(total_x/math.sin(self.hor_fov))*math.sin(self.hor_rem)
        print(z_h)
        dist=math.cos(self.hor_fov/2)*z_h
        print(f"dist is {dist}")
        z_v=(total_y/math.sin(self.ver_fov))*math.sin(self.ver_rem)
        dist2 = math.cos(self.ver_fov/2)*z_v

        # average distances determined through Y and X to get idea # 
        self.distance= (dist+dist2)/2
        if self.x==5:
            print(f"currently at distance {self.distance}")
            self.x=0
        

    def calc_arrow_drop(self, h): #y_val is the y distance value for target: h 
        """grabs the angle and the velocity to find how far the 
        arrow will fall from the distance to the target
        conversion between feet and pixels"""

        #grab the angle from the other program
        t_t_h = self.distance/self.PH.calc_speed() #stands for time to hit // I don't think this works
        
        print(f"time to hit is {t_t_h}")
        upward_vel = self.PH.calc_speed()*math.sin(0)
       

        # dist_lower value is negative, meaning just add it to the other stuff
        #convert actual distance to pixels on screen, based on how far away I'm standing. 
        
        dist_lower =  (t_t_h*upward_vel) + (.5*(-9.81)*(t_t_h**2)) # in meters
        print(f"distance lower: {dist_lower}")
        pixels_down = dist_lower*self.ratio  # should convert the feet to pixels

        return(int(pixels_down))

if __name__ == "__main__":
    RT = RunThrough()
    RT.runner()