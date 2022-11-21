from app.api.upload_robot import Body
import base64


square_script = """from robots.Robot import Robot
class SquareBot(Robot):
    
    def initialize(self):
        super().is_cannon_ready()
        super().get_position()
        self.direction = 230
        self.turncount = 2
        
    def respond(self):
        super().drive(self.direction, 40)
        self.turncount -= 1
        if self.turncount == 0:
            self.direction = (self.direction + 90) % 360
            self.turncount = 2
  """

SquareBot = Body(
    name="Square Bot",
    avatar= (b'data:image/jpg;base64,' + base64.b64encode(open("robots/default_robots/SquareBot_avatar.jpg", "rb").read())),
    script= square_script,
    fileName="SquareBot.py",
    )
