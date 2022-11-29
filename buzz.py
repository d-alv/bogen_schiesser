from gpiozero import RGBLED 
from gpiozero import Button 
from enum import Enum
import time

# honestly buzzing feature kind of sucks, not that accurate, maybe 
# change with a screen or something?
# change this to an LED or something on the bow? 
class Precision(Enum):
    Low: int=3
    Med: int=2
    High: int=1

class Buzzing:
    """class for running the buzzing to show
    if the bow is close to target"""
    def __init__(self):
        self.led = RGBLED(21, 20, 26) #bottom_right pin, 20= one above it, and 26 = one left to 20
        self.color= [0,0,0]
        self.x=0
        self.but = Button(16) # this is right above 20
        self.accuracy = Precision(3)
        # if no target detected = blue, if missing = red, if on target = green
        self.color_flag=False
        self.stime=0
        self.elapsed_time=0
        self.ratio=0

    def buzz_now(self, net_pos, hit=False):
        
        """uses net position to determine freq
        and hit plays a double beep when on target"""
        if not self.color_flag:
            self.x+=1

            if not hit:
                if net_pos <300:
                    point = float(-net_pos/300)+1
                    #smaller net position = greener
                    # point represents green, green and red are inverse
                    self.color[1] = round(point, 2)
                    self.color[0] = round(1-point, 2)
                    print(self.color)
                    color= tuple(self.color)
                    self.led.color = color
                else:
                    self.led.color=(0,0,1)

            else: 
                self.led.color = (0, 1, 0)

    def no_targ(self):
        self.led.color=(0,0,1) #blue

    def press_check(self):

        if self.color_flag:
            self.check_time()
            if self.elapsed_time>3:
                self.color_flag=False
            # check the time - update time 

        if self.but.is_pressed:
            if not self.color_flag:
                self.color_flag=True
                self.start_flag(self.accuracy.value)

                # turn on LED and start timer
            else:
                
                if self.accuracy==Precision(3):
                    self.accuracy=Precision(2)
                    self.ratio=.4
                
                if self.accuracy==Precision(2):
                    self.accuracy=Precision(1)
                    self.ratio=.25
                
                if self.accuracy==Precision(1):
                    self.accuracy=Precision(3)
                    self.ratio=0
                self.start_flag(self.accuracy.value)
                    # ratio closer to one means more precise! 
    def start_flag(self, value):
        if value==1:
            self.led.color = (0,1,0)
        elif value==2:
            self.led.color = (1,1,0)
        elif value==3:
            self.led.color = (1,0,0)
        self.set_start()

    def check_time(self):
        """method for constantly checking time -
            specifically useful for phone ringing and
            no answer - don't need RTC module since WIFI"""
        self.elapsed_time = time.time() - self.stime
        
    def set_start(self):
        """method sets timer to zero"""
        self.stime = time.time()

    # I want it to flash the current 