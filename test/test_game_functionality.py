# import sys
# sys.path.insert(0, "./robots")
# from robots.Robot import *
# from robots.Juego import *
# from robots.Partida import *
# #import Missile as ms
# from math import isclose
# test_robots = ["robots/files/admin/TestBot.py", "robots/files/admin1/TestBot.py"]
# MAX_SPEED = 25

# def compare_positions(p1, p2):
#     return isclose(p1[0], p2[0]) and isclose(p1[1], p2[1])

# def test_simulation():
#     game = Juego(["robots/files/admin/CircleBot.py", "robots/files/admin/SquareBot.py"], 10, is_simulation = True)
#     game.run()
#     res = game.get_results()
#     assert isinstance(res, dict)
#     assert isinstance(res["rounds"], list)
#     assert isinstance(res["rounds"][0], dict)
#     assert isinstance(res["rounds"][0]["robots"], list)
#     assert isinstance(res["rounds"][0]["robots"][0], dict)
#     assert isinstance(res["rounds"][0]["missiles"], list)
#     assert isinstance(res["rounds"][0]["missiles"][0], dict)
    
# def test_single_game():
#     game = Juego(["robots/files/admin/CircleBot.py", "robots/files/admin/SquareBot.py"], 10, is_simulation = False)
#     game.run()
#     assert isinstance(game.get_results(), str)

# def test_move_bots():
#     game = Juego(["robots/files/admin/TestBot.py", "robots/files/admin1/TestBot.py"], 10, is_simulation = False)
#     game.instantiate_bots()
#     game.initialize_bots()
#     p1 = game.robots[0].get_position()
#     p2 = game.robots[1].get_position()

#     for i in range(50):
#         game.respond_bots()
#         game.move_bots()
#         expected_x1 = min(max(0, p1[0] + MAX_SPEED), 1000)
#         expected_x2 = min(max(0, p2[0] + MAX_SPEED), 1000)
#         assert compare_positions((expected_x1, p1[1]), game.robots[0].get_position())
#         assert compare_positions((expected_x2, p2[1]), game.robots[1].get_position())
#         p1 = game.robots[0].get_position()
#         p2 = game.robots[1].get_position()
    
# def test_partida():
#     bot_list = ["robots/files/admin/CircleBot.py", "robots/files/admin1/SquareBot.py", "robots/files/admin2/SuperMegaRobot.py"]
#     partida = Partida(bot_list, {"games":10, "rounds":200})
#     partida.run()
#     res = partida.get_results()
#     assert isinstance(res, list)
#     for winner in res:
#         assert isinstance(winner, dict)
#         assert "robots/files/{}/{}.py".format(winner["user"], winner["robot"]) in bot_list
    
