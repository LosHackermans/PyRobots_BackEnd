import sys
sys.path.insert(0, "./robots")
from Robot import *
import Missile as ms
from math import isclose

def test_instantiate_robot():
    robot_1 = Robot(50, 50)
    assert robot_1.get_position() == (50, 50)
    assert robot_1.get_direction() == 0
    assert robot_1.get_damage() == 0
    assert robot_1.get_velocity() == 0
    assert robot_1.scanned() == 0
    assert robot_1.is_cannon_ready() == True
    assert robot_1.data["cannon_ready"] == True
    assert robot_1.data["cannon_degree"] == 0
    assert robot_1.data["cannon_distance"] == 0
    assert robot_1.data["scanner_direction"] == 0
    assert robot_1.data["scanner_resolution"] == 0
    assert robot_1.data["alive"] == True
    assert robot_1.data["intends_to_shoot"] == False
    assert robot_1.data["shot_last_round"] == False
    
    robot_negativo = Robot(-10, -10)
    assert robot_negativo.get_position() == (0, 0)
    assert robot_negativo.get_direction() == 0
    assert robot_negativo.get_damage() == 0
    assert robot_negativo.get_velocity() == 0
    assert robot_negativo.scanned() == 0
    assert robot_negativo.is_cannon_ready() == True
    assert robot_negativo.data["cannon_ready"] == True
    assert robot_negativo.data["cannon_degree"] == 0
    assert robot_negativo.data["cannon_distance"] == 0
    assert robot_negativo.data["scanner_direction"] == 0
    assert robot_negativo.data["scanner_resolution"] == 0
    assert robot_negativo.data["alive"] == True
    assert robot_negativo.data["intends_to_shoot"] == False
    assert robot_negativo.data["shot_last_round"] == False
    

def test_move_robot():
    robot_1 = Robot(50, 50)
    robot_1.drive(50, 100)
    assert robot_1.get_direction() == 50
    assert robot_1.get_velocity() == 100
    
    robot_1.drive(500, 400)
    assert robot_1.get_direction() == 50
    assert robot_1.get_velocity() == 100
    
    robot_1.drive(20, 30)
    assert robot_1.get_direction() == 20
    assert robot_1.get_velocity() == 30
    
    robot_1.drive(-1, -1)
    assert robot_1.get_direction() == 20
    assert robot_1.get_velocity() == 30
    

def test_use_radar():
    robot_1 = Robot(50, 50)
    robot_2 = Robot(50, 100)
    robot_3 = Robot(500, 50)
    enemy_positions = [robot_2.get_position()]
    enemy_positions.append(robot_3.get_position())
    
    assert robot_1.scanned() == 0
    assert robot_1.data["scanner_direction"] == 0
    assert robot_1.data["scanner_resolution"] == 0
    
    robot_1.point_scanner(300, 1)
    robot_1.scan(enemy_positions)
    assert robot_1.data["scanner_direction"] == 300
    assert robot_1.data["scanner_resolution"] == 1
    assert robot_1.scanned() == -1
    
    robot_1.point_scanner(379, 15)
    robot_1.scan(enemy_positions)
    assert robot_1.data["scanner_direction"] == 300
    assert robot_1.data["scanner_resolution"] == 1
    assert robot_1.scanned() == -1
    
    robot_1.point_scanner(-1, -1)
    robot_1.scan(enemy_positions)
    assert robot_1.data["scanner_direction"] == 300
    assert robot_1.data["scanner_resolution"] == 1
    assert robot_1.scanned() == -1

    robot_1.point_scanner(90, 5)
    robot_1.scan(enemy_positions)
    assert robot_1.data["scanner_direction"] == 90
    assert robot_1.data["scanner_resolution"] == 5
    assert robot_1.scanned() == 50

    robot_1.point_scanner(0, 10)
    robot_1.scan(enemy_positions)
    assert robot_1.data["scanner_direction"] == 0
    assert robot_1.data["scanner_resolution"] == 10
    assert robot_1.scanned() == 450
    
    robot_1.point_scanner(0, 0)
    robot_1.scan(enemy_positions)
    assert robot_1.data["scanner_direction"] == 0
    assert robot_1.data["scanner_resolution"] == 0
    assert robot_1.scanned() == 450

def test_use_cannon():
    robot_1 = Robot(50, 50)
    assert robot_1.is_cannon_ready() == True
    assert robot_1.data["cannon_degree"] == 0
    assert robot_1.data["cannon_distance"] == 0
    
    robot_1.cannon(123, 650)
    assert robot_1.data["cannon_degree"] == 123
    assert robot_1.data["cannon_distance"] == 650
    
    robot_1.cannon(600, 1000)
    assert robot_1.data["cannon_degree"] == 123
    assert robot_1.data["cannon_distance"] == 650
    
    robot_1.cannon(20, 10)
    assert robot_1.data["cannon_degree"] == 20
    assert robot_1.data["cannon_distance"] == 10
    
    robot_1.cannon(-1, -1)
    assert robot_1.data["cannon_degree"] == 20
    assert robot_1.data["cannon_distance"] == 10
    
    assert robot_1.is_cannon_ready() == True
    assert robot_1.spend_cannon() == True
    assert robot_1.spend_cannon() == False
    assert robot_1.is_cannon_ready() == False
    
    robot_1.ready_cannon()
    assert robot_1.is_cannon_ready() == True
    assert robot_1.spend_cannon() == True
    assert robot_1.spend_cannon() == False
    assert robot_1.is_cannon_ready() == False
    
# def test_missiles():
#     m1 = ms.Missile(100, 100, 90, 500)
#     m2 = ms.Missile(500, 500, 0, 200)
#     m3 = ms.Missile(900, 900, 90, 400)
    
#     assert m1.get_position() == (100, 100)
#     assert m1.is_exploded() == False
#     assert m2.get_position() == (500, 500)
#     assert m2.is_exploded() == False
#     assert m3.get_position() == (900, 900)
#     assert m3.is_exploded() == False
    
#     (e, x, y) = m1.update()
#     assert not e and isclose(x, 100) and isclose(y, 250)
#     (e, x, y) = m2.update()
#     assert not e and isclose(x, 650) and isclose(y, 500)
#     (e, x, y) = m3.update()
#     assert e and isclose(x, 900) and isclose(y, 1000)
#     assert m3.explosion_damage((900, 1000)) == 50

#     (e, x, y) = m1.update()
#     assert not e and isclose(x, 100) and isclose(y, 400)
#     (e, x, y) = m2.update()
#     assert e and isclose(x, 700) and isclose(y, 500)
#     assert m2.explosion_damage((710, 515)) == 50
    
#     (e, x, y) = m1.update()
#     assert not e and isclose(x, 100) and isclose(y, 550)
    
#     (e, x, y) = m1.update()
#     assert e and isclose(x, 100) and isclose(y, 600)
#     assert m1.explosion_damage((100, 100)) == 0
    
    

