from Map import Map

class Robot():
#Funciones auxiliares, el usuario no las conoce    
    def __init__(self, pos_x: int, pos_y: int, direction)
        self.data = {}
        self.data["pos_x"] = pos_x
        self.data["pos_y"] = pos_y
        self.data["health"] = 100
        self.data["direction"] = 0
        self.data["velocity"] = 0
        self.data["cannon"] = True
        self.data["cannon_degree"] = 0
        self.data["cannon_distance"] = 0
        self.data["scanner_direction"] = 0
        self.data["scanner_resolution"] = 0
        self.data["scanned"] = 0
        
        
    def __get_data(self):
        return self.data
    
    def __ready_cannon(self):
        if not self.data["cannon"]:
            self.data["cannon"] = True
            
    def __spend_cannon(self):
        self.data["cannon"] = False

    def __es_numero(a):
        return (type(a) == int or type(a) == float) and a >= 0

#funciones publicas
    def is_cannon_ready(self):
        return cannon_ready
    
    def cannon(self, degree, distance):
        #print("llamada a cannon(%s, %s)" % (degree, distance))
        if __es_numero(degree) and __es_numero(distance) and degree < 360 and distance < 700:
            self.data["cannon_degree"] = degree
            self.data["cannon_distance"] = distance
        
    def point_scanner(self, direction, resolution):
        #print("llamada a point_scanner(%s, %s)" % (direction, resolution_in_degrees))
        if __es_numero(direction) and __es_numero(resolution) and direction < 360 and resolution <= 10:
            self.data["scanner_direction"] = direction
            self.data["scanner_resolution"] = resolution
        
    def scanned(self):
        return self.data["scanned"]
        
    def drive(self, direction, velocity):
        #print("llamada a drive(%s, %s)" % (direction, velocity))
        if __es_numero(direction) and __es_numero(velocity) and direction < 360 and velocity <= 100:
            self.data["direction"] = direction
            self.data["velocity"] = velocity
        
    def get_direction(self):
        return self.direction
        
    def get_velocity(self):
        return self.engine_velocity
        
    def get_position(self):
        return self.position
        
    def get_damage(self):
        return 100 - self.data["health"]
