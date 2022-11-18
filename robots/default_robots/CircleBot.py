from app.api.upload_robot import Body


circle_script = """from robots.Robot import Robot
class CircleBot(Robot):
    
    def initialize(self):
        super().is_cannon_ready()
        super().get_position()
        self.direction = 80
        
    def respond(self):
        super().drive(self.direction, 30)
        self.direction = (self.direction + 10) % 360
        super().cannon(180, 600)
  """

circle_avatar = ""

CircleBot = Body(
    name="Circle Bot",
    avatar= circle_avatar,
    script= circle_script,
    fileName="CircleBot.py",
    )
