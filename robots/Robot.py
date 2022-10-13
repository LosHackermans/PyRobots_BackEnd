    

class Robot():

    def is_cannon_ready(self):
        print("llamada a is_cannon_ready")
    
    def cannon(self, degree, distance):
        print("llamada a cannon(%s, %s)" % (degree, distance))
        
    def point_scanner(self, direction, resolution_in_degrees):
        print("llamada a point_scanner(%s, %s)" % (direction, resolution_in_degrees))
        
    def scanned(self):
        print("llamada a scanned")
        
    def drive(self, direction, velocity):
        print("llamada a drive(%s, %s)" % (direction, velocity))
        
    def get_direction(self):
        print("llamada a get_direction")
        
    def get_velocity(self):
        print("llamada a get_velocity")
        
    def get_position(self):
        print("llamada a get_position")
        
    def get_damage(self):
        print("llamada a get_damage")
    
