# as far as I can tell, this file will not be used anymore
#this is because i do not believe the angle is very important to be measured for the bow unless at 
# VERY sharp angles - likely not come back to this file

import RPi.GPIO as GPIO
import time 
import math

GPIO.setmode(GPIO.BCM)

pin_a = 18
pin_b = 24

class Angle:
    def __init__(self):
        """define variables n such"""
        self.rad = 0

    def discharge(self):
        GPIO.setup(pin_a, GPIO.IN)
        GPIO.setup(pin_b, GPIO.OUT)
        GPIO.output(pin_b, False)
        time.sleep(.008)

    def charge_time(self):
        GPIO.setup(pin_b, GPIO.IN)
        GPIO.setup(pin_a, GPIO.OUT)
        count =0
        GPIO.output(pin_a, True)
        while not GPIO.input(pin_b):
            count = count+1

        x=1851.851 #iterator of sorts, every 1851 is next degree

        absolute_degree = 0 #set to perfectly straight 0 @ 20000
        degree = (count/x)-23
        degree = -degree-16
        

        self.rad = (degree/180)*math.pi
        
        return self.rad

    def analog_read(self):
        #print("reading")
        #time.sleep(.5)
        self.discharge()
        self.charge_time()
        return self.rad


#dog = Angle()
#while True:
    
 #   print(f"currently at {dog.analog_read()} degrees")
  #  time.sleep(.5)
