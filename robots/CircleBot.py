import Robot
class CircleBot(Robot.Robot):
    
    def initialize(self):
        super().is_cannon_ready()
        super().get_position()
        self.direction = 80
        
    def respond(self):
        super().drive(self.direction, 30)
        self.direction = (self.direction + 10) % 360
        super().cannon(180, 500)
