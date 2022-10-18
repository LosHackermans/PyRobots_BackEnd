from time import sleep
import SuperMegaRobot as smr

class BotScheduler():
    

    def __init__(self):
        print("init de BotScheduler")
        self.robots = []
        self.instantiate_bots()
        self.initialize_bots()
        self.run_bots()
        
    def instantiate_bots(self):
        self.robots.append(smr.SuperMegaRobot())
    
    def initialize_bots(self):
        for bot in self.robots:
            bot.initialize()
    
    def run_bots(self):
        for i in range(10):
            for bot in self.robots:
                bot.respond()
                
            sleep(3)



if __name__=="__main__":
    print("main de BotScheduler")
    BotScheduler()
    
