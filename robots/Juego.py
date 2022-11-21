from time import sleep
from robots.Robot import *
from robots.Missile import Missile
from random import randrange
from math import cos, sin, pi
from robots.GameState import *

MAX_SPEED = 25
WALL_DAMAGE = 10

def to_rads(x):
    return x * (pi / 180)

create_bot_string = """
from robots.files.{}.{} import *
self.bot = {}({}, {})
"""

class Juego:
    
    def __init__(self, bot_list, rounds, is_simulation = True):
        self.bot_list = bot_list
        self.rounds = rounds
        self.missiles = []
        self.robots = []
        
        self.simulation = is_simulation
        if self.simulation:
            self.game_state = GameState()
        
    def instantiate_bots(self):
        for filestring in self.bot_list:
            spawn = (randrange(0, 1000, 20), randrange(0, 1000, 20))
            user_id, botname = filestring[len("robots/files/"):].split('/')
            exec(create_bot_string.format(user_id, botname[:-3], botname[:-3], spawn[0], spawn[1]))
            self.bot.data["bot_id"] = botname[:-3]
            self.robots.append(self.bot)
        
    def initialize_bots(self):
        for bot in self.robots:
            bot.initialize()
    
    def run(self):
        self.instantiate_bots()
        self.initialize_bots()
        for i in range(self.rounds):
            self.respond_bots()
            self.move_bots()
            self.update_scanners()
            self.shoot_cannons()
            self.update_missiles()
            self.reload_cannons()
            if self.simulation:
                self.game_state.commit_game_state()
    
    def respond_bots(self):
        for bot in self.robots:
            if bot.is_alive():
                bot.respond()

    def move_bots(self):
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
            if self.simulation:
                self.game_state.add_bot(bot.get_id(), bot.get_position(), 100 - bot.get_damage())
        
    def update_scanners(self):
        for bot in self.robots:
            enemy_positions = []
            for e in self.robots:
                if e.get_position() != bot.get_position():
                    enemy_positions.append(e.get_position())
            bot.scan(enemy_positions)


    def shoot_cannons(self):
        for bot in self.robots:
            if bot.is_cannon_ready() and bot.data["intends_to_shoot"]:
                x, y = bot.get_position()
                self.missiles.append(Missile(x, y, bot.data["cannon_degree"], bot.data["cannon_distance"], bot.get_id()))
                bot.data["intends_to_shoot"] = False
                bot.spend_cannon()
    
    def reload_cannons(self):
        for bot in self.robots:
            bot.reload_cannons()
        
    def update_missiles(self):
        for missile in self.missiles:
            status = missile.update()
            if self.simulation:
                self.game_state.add_missile(missile.get_position(), status[0], missile.shooter)
            if status[0]:
                for bot in self.robots:
                    bot.receive_damage(missile.explosion_damage(bot.get_position()))
                self.missiles.remove(missile)
                
    def get_results(self):
        winning_bots = []
        winner = ""
        for bot in self.robots:
            if bot.is_alive():
                winning_bots.append(bot) 
        if len(winning_bots) == 1:
            winner = winning_bots[0].get_id()
        else:
            winner = "EMPATE"
            
        return self.game_state.produce_final_json() if self.simulation else winner


if __name__ == "__main__":
    game = Juego(["robots/files/admin/CircleBot.py", "robots/files/admin/SquareBot.py", "robots/files/admin/SuperMegaRobot.py"], 10, False)
    game.run()
    print(game.get_results())
