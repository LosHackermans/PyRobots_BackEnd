from robots.Scanner import scan_enemies

class Robot:
#Funciones auxiliares, el usuario no las conoce    
    def __init__(self, pos_x, pos_y):
        self.data = {}
        self.data["bot_id"] = ""
        if self.__es_numero(pos_x) and self.__es_numero(pos_y):
            self.data["pos_x"] = pos_x
            self.data["pos_y"] = pos_y
        else:
            self.data["pos_x"] = 0
            self.data["pos_y"] = 0
        self.data["health"] = 100
        self.data["alive"] = True
        self.data["direction"] = 0
        self.data["velocity"] = 0
        self.data["cannon_ready"] = True
        self.data["intends_to_shoot"] = False
        self.data["shot_last_round"] = False
        self.data["cannon_degree"] = 0
        self.data["cannon_distance"] = 0
        self.data["scanner_direction"] = 0
        self.data["scanner_resolution"] = 0
        self.data["scanned"] = 0
        
    def get_id(self):
        return self.data["bot_id"]
        
    def get_data(self):
        return self.data
    
    def ready_cannon(self):
        if not self.data["cannon_ready"]:
            self.data["cannon_ready"] = True
            
    def spend_cannon(self):
        was_ready = self.data["cannon_ready"]
        if was_ready:
            self.data["cannon_ready"] = False
            self.data["shot_last_round"] = True
        return was_ready
        
    def set_position(self, x, y):
        self.data["pos_x"] = x
        self.data["pos_y"] = y

    def receive_damage(self, dmg):
        self.data["health"] -= dmg
        if self.data["health"] <= 0:
            self.data["health"] = 0
            self.data["alive"] = False
            
    def is_alive(self):
        return self.data["alive"]
        
    def reload_cannons(self):
        if self.data["shot_last_round"]:
            self.data["shot_last_round"] = False
        else:
            self.data["cannon_ready"] = True
            
    def scan(self, enemies): 
        self.data["scanned"] = scan_enemies(self.get_position(), enemies, self.data["scanner_direction"], self.data["scanner_resolution"])

    def __es_numero(self, a):
        return (type(a) == int or type(a) == float) and a >= 0

#funciones publicas
    def cannon(self, degree, distance):
        if self.__es_numero(degree) and self.__es_numero(distance) and degree < 360 and distance < 700:
            self.data["cannon_degree"] = degree
            self.data["cannon_distance"] = distance
            self.data["intends_to_shoot"] = True

    def is_cannon_ready(self):
        return self.data["cannon_ready"]
    
    def point_scanner(self, direction, resolution):
        if self.__es_numero(direction) and self.__es_numero(resolution) and direction < 360 and resolution <= 10:
            self.data["scanner_direction"] = direction
            self.data["scanner_resolution"] = resolution
        
    def scanned(self):
        return self.data["scanned"]
        
    def drive(self, direction, velocity):
        if self.__es_numero(direction) and self.__es_numero(velocity) and direction < 360 and velocity <= 100:
            self.data["direction"] = direction
            self.data["velocity"] = velocity
        
    def get_direction(self):
        return self.data["direction"]
        
    def get_velocity(self):
        return self.data["velocity"]
        
    def get_position(self):
        return (self.data["pos_x"], self.data["pos_y"])
        
    def get_damage(self):
        return 100 - self.data["health"]
