from gpiozero import RGBLED 

# honestly buzzing feature kind of sucks, not that accurate, maybe 
# change with a screen or something?
# change this to an LED or something on the bow? 


class Buzzing:
    """class for running the buzzing to show
    if the bow is close to target"""
    def __init__(self):
        self.led = RGBLED(21, 20, 26) #bottom_right pin, 20= one above it, and 26 = one left to 20
        self.color= [0,0,0]
        self.x=0
        # if no target detected = blue, if missing = red, if on target = green

    def buzz_now(self, net_pos, hit=False):
        """uses net position to determine freq
        and hit plays a double beep when on target"""
        self.x+=1

        if not hit:
            if net_pos <200:
                point = float(-net_pos/200)+1
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