from robots.Juego import *

class Partida:
    def __init__(self, bot_list, config_partida):
        print("init de Partida")
        self.bot_list = bot_list
        self.games = config_partida["games"]
        self.game_rounds = config_partida["rounds"]
        "self.players = config_partida["players"]
        
        
        
    def run(self):
        self.scores = {"EMPATE": 0}
        for bot in self.bot_list:
            self.scores[f"{bot.get_id()}"] = 0
            
        for i in range(self.games):
            game = Juego(bot_list, self.rounds)
            winner = game.get_results(simulacion = False)
            self.scores[f"{winner}"] += 1
            
        result = [key for key, value in self.scores.items() if value == max(self.scores.values())]
        output = "EMPATE" if len(result) > 1 else max(self.scores, key=self.scores.get)
        return output




if __name__=="__main__":
    print("main de Partida")
    Partida(["robots/files/admin/CircleBot.py", "robots/files/admin/SquareBot.py", "robots/files/admin/SuperMegaRobot.py"], {"games":10, "rounds":200, "players":3})
    print(Partida.run())
    
