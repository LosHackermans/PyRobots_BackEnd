from time import sleep
from Robot import *
from random import randrange

bots_hardcodeados = ["CircleBot.py", "SquareBot.py", "SuperMegaRobot.py"]

create_bot_string = """
from Robot import *
from {} import *
self.bot = {}({}, {})
"""

class Juego:
    
    def __init__(self, bot_list):
        print("init de Juego")
        self.bot_list = bot_list
        self.instantiate_bots()
        self.initialize_bots()
        self.run_bots()
        
    def instantiate_bots(self):
        self.robots = []
        for botname in self.bot_list:
            spawn = (randrange(0, 1000, 20), randrange(0, 1000, 20))
            exec(create_bot_string.format(botname[:-3], botname[:-3], spawn[0], spawn[1]))
            self.robots.append(self.bot)
            print(self.bot.get_position())
        
    def initialize_bots(self):
        for bot in self.robots:
            bot.initialize()
    
    def run_bots(self):
        print("runbots")
        for i in range(10):
            for bot in self.robots:
                bot.respond()
                
            sleep(1)



if __name__=="__main__":
    print("main de Partida")
    Juego(bots_hardcodeados)
    
