from math import cos, sin, pi, sqrt
MISSILE_SPEED = 50
EXPLOSION_RADIUS = 100
EXPLOSION_DAMAGE = 25

def to_rads(x):
    return x * (pi / 180)

class Missile:
    def __init__(self, x, y, direction, distance, shooter):
        self.pos = (x, y)
        self.direction = direction
        self.remaining_distance = distance
        self.exploded = False
        self.shooter = shooter
        
    def update(self):
        prev_x = self.pos[0]
        prev_y = self.pos[1]
        H = min(MISSILE_SPEED, self.remaining_distance)
        self.remaining_distance -= H
        next_x = prev_x + cos(to_rads(self.direction)) * H
        next_y = prev_y + sin(to_rads(self.direction)) * H
        if next_x >= 1000:
            next_x = 1000
            self.exploded = True
        if next_y >= 1000:
            next_y = 1000
            self.exploded = True
        if next_x <= 0:
            next_x = 0
            self.exploded = True
        if next_y <= 0:
            next_y = 0
            self.exploded = True
        if self.remaining_distance <= 0:
            self.exploded = True
        ##TODO buscar una forma mas fancy de hacer esto, tipo max(0, min(1000, prev_x)) 
        self.pos = (next_x, next_y)
        return (self.exploded, self.pos[0], self.pos[1])

    def explosion_damage(self, target_pos):
        dist_to_center = sqrt((abs(self.pos[0] - target_pos[0]))**2 + (abs(self.pos[1] - target_pos[1]))**2)
        return EXPLOSION_DAMAGE if dist_to_center <= EXPLOSION_RADIUS else 0
        
    def get_position(self):
        return self.pos

    def is_exploded(self):
        return self.exploded


