from app.api.upload_robot import Body
import base64


circle_script = """from robots.Robot import Robot
class CircleBot(Robot):
    
    def initialize(self):
        super().is_cannon_ready()
        super().get_position()
        self.direction = 80
        
    def respond(self):
        super().drive(self.direction, 30)
        self.direction = (self.direction + 10) % 360
        super().cannon(self.direction, 300)
  """

CircleBot = Body(
    name="Circle Bot",
    avatar= (b'data:image/jpg;base64,' + base64.b64encode(open("robots/default_robots/CircleBot_avatar.jpg", "rb").read())),
    script= circle_script,
    fileName="CircleBot.py",
    )
