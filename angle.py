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
        time.sleep(.003)

    def charge_time(self):
        GPIO.setup(pin_b, GPIO.IN)
        GPIO.setup(pin_a, GPIO.OUT)
        count =0
        GPIO.output(pin_a, True)
        while not GPIO.input(pin_b):
            count = count+1

        x=1851.851 #iterator of sorts, every 1851 is next degree

        absolute_degree = 0 #set to perfectly straight
        degree = (count/x)-54
        if degree >0:
            degree = 0-degree
        else:
            degree = 0-degree #if negative, turns positive

        self.rad = (degree/180)*math.pi
        return self.rad

    def analog_read(self):
        print("reading")
        self.discharge()
        return self.charge_time()


# while True:
#     print(analog_read())
#     #time.sleep(1)