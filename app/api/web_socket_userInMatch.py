from fastapi import FastAPI, Request, HTTPException, status, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.api.models import *
from fastapi.encoders import jsonable_encoder
from typing import Optional
from pony.orm import db_session
from fastapi import APIRouter

router = APIRouter()


@router.websocket("/") #falta agregar ruta de la funcion
async def webssocket_endpoint_match(websocket: WebSocket):
        print("Accepting connection")
        await websocket.accept()
        print("Accepted")

        await_data = await websocket.receive_json() #recieve.text() 
        match_id = await_data["id"]
        list_of_players = []
        robot_of_the_cretor_id = 0

        with db_session:
            The_Match = Match.get(lambda m: m.id == match_id)
            while True:
                try: 
                    ##Buscar partida y sus participantes
                    for robot_o in The_Match.robot_in_matches:
                        if (robot_o.user.id == The_Match.user.id):
                            robot_of_the_cretor = robot_o.name
                            robot_of_the_cretor_id = robot_o.id
                            match_creator = {"Owner": The_Match.user.name, "Robot_name": robot_of_the_cretor}
                        else:
                            match_creator = {"Owner": The_Match.user.name, "Robot_name": "Unknown"}

                    for robot in Match.robot_in_matches:
                        if (robot.id == robot_of_the_cretor_id):
                            pass
                        else:
                            robot_name = robot.name
                            robot_id = robot.id
                            robot_user = Robot.get(lambda r: r.id == robot_id)
                            user_of_the_robot = robot_user.user.name

                            the_player = {"Player": user_of_the_robot, "Robot_name": robot_name}
                            list_of_players.append(the_player)


                    json_players = {"Creator": match_creator, "Players": list_of_players}
                    await websocket.send_json(json_players) #send_text()
            
                except:
                    pass
                    break



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