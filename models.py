from pony.orm import *


db = Database()


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str)
    email = Required(str)
    password = Required(str)
    avatar = Optional(str)
    is_validated = Required(bool)
    robots = Set('Robot')
    matches = Set('Match')


class Robot(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    avatar = Optional(str)
    script = Required(LongStr)
    user = Required(User)
    robot_in_matches = Set('Robot_in_match')


class Match(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    min_players = Required(int)
    max_players = Required(int)
    number_rounds = Required(int)
    number_games = Required(int)
    user = Required(User)
    robot_in_matches = Set('Robot_in_match')


class Robot_in_match(db.Entity):
    robot = Required(Robot)
    games_won = Required(int)
    games_draw = Required(int)
    match = Required(Match)

