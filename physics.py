import math

# use this class probably to do the maths behind it

class PH:
    def __init__(self):
        """this is where I define the physics values and can also
        change these values real time"""
        self.arrow_mass = .0162
        self.force = 197.94
        self.l_angle = 0
        self.draw_length = .6858 #just putting a value here for now - somewhat realistic
        self.k_const = 288.63
        


    def calc_speed(self):
        elast_pot = .5*self.k_const*self.draw_length
        kinet_pot = .94*elast_pot
        arrow_speed = math.sqrt((kinet_pot*2)/self.arrow_mass) #
        return(arrow_speed)

    
