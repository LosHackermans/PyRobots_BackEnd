import sys
sys.path.insert(0, "./robots")
from Robot import *

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
    
    robot_negativo = Robot(-10, -10)
    assert robot_negativo.get_position() == (0, 0)
    

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
    assert robot_1.scanned() == 0
    assert robot_1.data["scanner_direction"] == 0
    assert robot_1.data["scanner_resolution"] == 0
    
    robot_1.point_scanner(300, 1)
    assert robot_1.data["scanner_direction"] == 300
    assert robot_1.data["scanner_resolution"] == 1
    
    robot_1.point_scanner(379, 15)
    assert robot_1.data["scanner_direction"] == 300
    assert robot_1.data["scanner_resolution"] == 1
    
    robot_1.point_scanner(-1, -1)
    assert robot_1.data["scanner_direction"] == 300
    assert robot_1.data["scanner_resolution"] == 1


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
