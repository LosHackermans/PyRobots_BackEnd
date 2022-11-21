from math import pi, atan2, sqrt

def to_deg(a):
    return a *(180/pi)
    
def to_rads(x):
    return x * (pi / 180)

def angle_to_enemy(bot_pos, enemy_pos):
    angle_x = enemy_pos[0] - bot_pos[0]
    angle_y = enemy_pos[1] - bot_pos[1]
    temp = to_deg(atan2(angle_y, angle_x))
    
    if angle_y < 0:
        result = temp + 360
    else:
        result = temp
    
    #print(f"para {angle_x}, {angle_y} ===> {result}°, ({temp})")
    return result

def distance_to_enemy(bot_pos, enemy_pos):
    return sqrt((enemy_pos[0] - bot_pos[0])**2 + (enemy_pos[1] - bot_pos[1])**2)

def scan_enemies(bot_pos, enemy_positions, scan_angle, resolution):
    distances = []
    
    for p in enemy_positions:
        if scan_angle - resolution <= angle_to_enemy(bot_pos, p) <= scan_angle + resolution:
            distances.append(distance_to_enemy(bot_pos, p))

    if len(distances) > 0:
        d = min(distances)
    else:
        d = -1

    return d
    
