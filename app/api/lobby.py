from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketState
from app.api.models import *
from pony.orm import db_session
from app.rooms import ConnectionManager
from robots.Partida import Partida

router = APIRouter()

manager = ConnectionManager()


def get_room(match_id):
    with db_session:
        The_Match = Match.get(lambda m: m.id == match_id)
        list_of_players = []
        robot_of_the_cretor_id = 0
        match_creator = {"Owner": "Unknown", "Robot_name": "Unknown"}
        # Buscar partida y sus participantes
        for robot_o in The_Match.robot_in_matches:
            if (robot_o.robot.user.id == The_Match.user.id):
                robot_of_the_cretor = robot_o.robot.name
                robot_of_the_cretor_id = robot_o.robot.id
                match_creator = {"Owner": The_Match.user.username,
                                 "Robot_name": robot_of_the_cretor}

            if (robot_o.robot.id != robot_of_the_cretor_id):
                robot_name = robot_o.robot.name
                robot_id = robot_o.robot.id
                robot_user = Robot.get(lambda r: r.id == robot_id)
                user_of_the_robot = robot_user.user.username
                the_player = {"Player": user_of_the_robot,
                              "Robot_name": robot_name}
                list_of_players.append(the_player)
    return {"Creator": match_creator, "Players": list_of_players}


def execute_match(match_id):
    
    # Descomentar esto para ejecutar el match
    with db_session:
       current_match = Match.get(lambda m: m.id == match_id)

       robots_query = Robot.select(lambda r: r in current_match.robot_in_matches.robot)
       robots_paths = [robot.script for robot in list(robots_query)]
    
       play_match = Partida ( robots_paths, 
                    {"games": current_match.number_games , "rounds": current_match.number_rounds}
                                  )
        
       play_match.run()
       return {"result": play_match.get_results()}
        #return {"result": "Pedrito", "robot": "pedritron"}

@router.websocket("/lobby/{match_id}")
async def webssocket_endpoint_match(websocket: WebSocket, match_id):
    await manager.connect(websocket, match_id)
    await manager.broadcast({"room" : get_room(match_id)}, match_id)
    try:
        while True:
            if websocket.application_state == WebSocketState.CONNECTED:
                data = await websocket.receive_text()
                if data == 'start':
                    results = execute_match(match_id)
                    await manager.broadcast(results, match_id)

    except Exception as e:
        print(e)
    finally:
        await manager.disconnect(websocket, match_id)

# {
#     Creator:
#
#              {"Owner": player_name, "Robot_name": name},
#     Players:
#             [
#              {"Player": player_name, "Robot_name": name},
#              {"Player": player_name, "Robot_name": name},
#              {"Player": player_name, "Robot_name": name}
#             ]
# }
