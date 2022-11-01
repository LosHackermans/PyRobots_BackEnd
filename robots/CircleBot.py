import Robot
class CircleBot(Robot.Robot):
    
    def initialize(self):
        super().is_cannon_ready()
        super().get_position()
        self.direction = super().get_direction()
        print("CircleBot ready!")
        
    def respond(self):
        super().drive(self.direction, 30)
        direction = (self.direction + 10) % 360
        print("CircleBot respond!")
