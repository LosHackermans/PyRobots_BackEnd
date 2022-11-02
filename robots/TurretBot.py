import Robot
from math import atan
from random import randrange

center = (500, 500)

class TurretBot(Robot.Robot):
    
    def initialize(self):

        self.direction = super().get_direction()
        
    def respond(self):
        self.pos = super().get_position()
        self.direction(atan((500 - super().get_position()[1]) / (500 - super().get_position()[0])))
        super().drive(self.direction, 30)
        self.angle = (self.angle + 40) % 360
        super().cannon(self.angle, randrange(100, 300))
        
        

