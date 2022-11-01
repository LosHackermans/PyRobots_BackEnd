from time import sleep
from Robot import *
from Missile import Missile
from random import randrange
from math import cos, sin, pi

bots_hardcodeados = ["CircleBot.py", "SquareBot.py", "SuperMegaRobot.py"]
MAX_SPEED = 100
WALL_DAMAGE = 10
MISSILE_DAMAGE = 25

def to_rads(x):
    return x * (pi / 180)

create_bot_string = """
from Robot import *
from {} import *
self.bot = {}({}, {})
"""

class Juego:
    
    def __init__(self, bot_list):
        self.bot_list = bot_list
        self.missiles = []
        self.instantiate_bots()
        self.initialize_bots()
        self.run_game()
        
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
    
    def run_game(self):
        for i in range(5):
            self.respond_bots()
            self.move_bots()
            self.update_scanners()
            self.shoot_cannons()
            self.update_missiles()
            self.record_game_state()
            sleep(1)
    
    def respond_bots(self):
        print("-------RESPOND BOTS")
        for bot in self.robots:
            bot.respond()

    def move_bots(self):
        print("-------MOVE BOTS")
        for bot in self.robots:
            prev_x, prev_y = bot.get_position()
            speed = bot.get_velocity()
            direction = bot.get_direction()
            
            H = (speed * MAX_SPEED) / 100
            next_x = prev_x + cos(to_rads(direction)) * H
            next_y = prev_y + sin(to_rads(direction)) * H
            if next_x >= 1000:
                bot.receive_damage(WALL_DAMAGE)
                next_x = 1000
            if next_y >= 1000:
                bot.receive_damage(WALL_DAMAGE)
                next_y = 1000
            if next_x <= 0:
                bot.receive_damage(WALL_DAMAGE)
                next_x = 0
            if next_y <= 0:
                bot.receive_damage(WALL_DAMAGE)
                next_y = 0
            ##TODO buscar una forma mas fancy de hacer esto, tipo max(0, min(1000, prev_x)) o extraer el método
            bot.set_position(next_x, next_y)
            print(f"bot {bot} movido de ({prev_x}, {prev_y}) a ({next_x}, {next_y}), mov= ({direction}, {speed})")
        
    def update_scanners(self):
        print("-------UPDATE SCANNERS")

    def shoot_cannons(self):
        print("-------SHOOT CANNONS")
        for bot in self.robots:
            if bot.is_cannon_ready() and bot.data["intends_to_shoot"]:
                x, y = bot.get_position()
                self.missiles.append(Missile(x, y, bot.data["cannon_degree"], bot.data["cannon_distance"]))
                print("cannon shot from ({}, {}) with direction {} and distance {}".format(x, y, bot.data["cannon_degree"], bot.data["cannon_distance"]))
        
    def update_missiles(self):
        print("-------UPDATE MISSILES")
        for missile in self.missiles:
            status = missile.update()
            if status[0]:
                print(f"missile exploded at ({status[1]}, {status[2]})")
                self.missiles.remove(missile)
            else:
                print(f"missile traveling at ({status[1]}, {status[2]}) with direction {missile.direction}, remaining travel {missile.remaining_distance}")
        
    def record_game_state(self):
        print("--------RECORD GAME STATE")
        

if __name__ == "__main__":
    Juego(bots_hardcodeados)
    
