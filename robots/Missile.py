from math import cos, sin, pi
MISSILE_SPEED = 350

def to_rads(x):
    return x * (pi / 180)

class Missile:
    def __init__(self, x, y, direction, distance):
        self.pos = (x, y)
        self.direction = direction
        self.remaining_distance = distance
        self.exploded = False
        
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
        print(f"{self.pos} ----->> ({next_x}, {next_y})")
        self.pos = (next_x, next_y)
        return (self.exploded, self.pos[0], self.pos[1])

    def get_position(self):
        return self.pos

    def is_exploded(self):
        return self.exploded
