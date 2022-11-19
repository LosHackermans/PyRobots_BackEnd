from robots.Juego import *

class Partida:
    def __init__(self, bot_list, config_partida):
        print("init de Partida")
        self.bot_list = bot_list
        self.scores, self.players = parse_bot_list(bot_list)        
        self.games = config_partida["games"]
        self.game_rounds = config_partida["rounds"]
        
    def run(self):
        for i in range(self.games):
            game = Juego(self.bot_list, self.game_rounds)
            #game.run_game()
            winner = game.get_results(simulacion = False)
            self.scores[f"{winner}"] += 1

        self.scores["EMPATE"] = 0
        results = [key for key, value in self.scores.items() if value == max(self.scores.values())]
        output = []
        for bot in results:
            output.append((bot, self.players[f"{bot}"]))
        return output


def parse_bot_list(bot_list):
    scores = {"EMPATE" : 0}
    players = {}
    
    for entry in bot_list:
        bot_name = entry.split('/')[-1][:-3]
        player_name = entry.split('/')[-2]
        scores[f"{bot_name}"] = 0
        players[f"{bot_name}"] = player_name

    return (scores, players)


if __name__=="__main__":
    print("main de Partida")
    p = Partida(["robots/files/admin/CircleBot.py", "robots/files/admin1/SquareBot.py", "robots/files/admin2/SuperMegaRobot.py"], {"games":10, "rounds":200})
    print(p.run())
    

