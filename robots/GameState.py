bot_string = "{{ id: {}, x: {}, y: {}, life: {}}}"
missile_string = "{{ x: {}, y: {}, exploded: {}}}"

class GameState:
    def __init__(self):
        self.state_strings = []
        self.bot_strings = []
        self.missile_strings = []
        
    def add_bot(self, bot_id, bot_pos, bot_health):
        self.bot_strings.append(bot_string.format(bot_id, bot_pos[0], bot_pos[1], bot_health))
        
    def add_missile(self, missile_pos, exploded):
        self.missile_strings.append(missile_string.format(missile_pos[0], missile_pos[1], exploded))
        
        
    def commit_game_state(self):
        #self.final_json += 
        state_string = ""
        state_string += "{\n\trobots: [\n" + "\t\t " + ', '.join(self.bot_strings) + "\n\t],\n"
        self.bot_strings = []
        state_string += "\tmissiles: [\n\t\t" + ', '.join(self.missile_strings) + "\n\t]\n}"
        self.missile_strings = []
        self.state_strings.append(state_string)
        
    def produce_final_json(self):
        return "{\nrounds: [\n" + ', '.join(self.state_strings) + "\n]\n}"
        
#{
#    rounds: [
#        {
#            robots: [
#                { id: , x: , y: , life:}, { id: , x: , y: , life:}
#            ],
#            missiles: [
#                { x, y, exploded }
#            ]
#        },
#        {
#            robots: [
#                { id: , x: , y: , life:}, { id: , x: , y: , life:}
#            ],
#            missiles: [
#                { x, y, exploded }
#            ]
#        }
#    ]
#}
