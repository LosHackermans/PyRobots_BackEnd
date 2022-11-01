import Robot
class SquareBot(Robot.Robot):
    
    def initialize(self):
        super().is_cannon_ready()
        super().get_position()
        self.direction = super().get_direction()
        self.turncount = 5
        print("SquareBot ready!")
        
    def respond(self):
        super().drive(self.direction, 40)
        self.turncount -= 1
        if self.turncount == 0:
            self.direction = (self.direction + 90) % 360
            self.turncount = 5
        print("SquareBot respond!")
