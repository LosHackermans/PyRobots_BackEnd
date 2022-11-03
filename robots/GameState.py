bot_string = "{{ id: {}, x: {}, y: {}, life: {}}}"
missile_string = "{{ x: {}, y: {}, exploded: {}}}"

class GameState:
    def __init__(self):
        self.state_strings = []
        self.bot_strings = []
        self.missile_strings = []
        
    def add_bot(self, bot_id, bot_pos, bot_health):
        self.bot_strings.append({"id": bot_id, "x": bot_pos[0], "y": bot_pos[1], "life": bot_health})
        
    def add_missile(self, missile_pos, exploded):
        self.missile_strings.append({"x": missile_pos[0], "y": missile_pos[1], "exploded": exploded})
        
        
    def commit_game_state(self):
        #self.final_json += 
        state_string = ""
        state_string = {"robots": self.bot_strings,
                        "missiles": self.missile_strings}
        self.bot_strings = []
        self.missile_strings = []
        self.state_strings.append(state_string)
        
    def produce_final_json(self):
        return {"rounds": self.state_strings}
        
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
