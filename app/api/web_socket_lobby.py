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
        robot_of_the_creator_id = 0

        match_is_start = False

        with db_session:
            while (len(list_of_players)<3 or match_is_start): #
                try: 
                    list_of_players = []

                    #recibe un json para ver si el match comenzo -> formato {"ready": bool}
                    #start_match = await websocket.receive_json()
                    #match_is_start = start_match["ready"]
                    ##############################################3

                    ##Buscar partida y sus participantes
                    The_Match = Match.get(lambda m: m.id == match_id)
                    for robot_o in The_Match.robot_in_matches: # SE PUEDE SELECCIONAR ASI?
                        if (robot_o.robot.user.id == The_Match.user.id): #SE PUEDE INSTANCIAR ASI?
                            robot_of_the_cretor = robot_o.robot.name
                            robot_of_the_creator_id = robot_o.robot.id
                            match_creator = {"Owner": The_Match.user.name, "Robot_name": robot_of_the_cretor}
                        else:
                            match_creator = {"Owner": The_Match.user.name, "Robot_name": "Unknown"}

                    for robot_o in Match.robot_in_matches:
                        if (robot_o.robot.id == robot_of_the_creator_id):
                            pass
                        else:
                            robot_name = robot_o.robot.name
                            robot_id = robot_o.robot.id
                            robot_user = Robot.get(lambda r: r.id == robot_id)
                            user_of_the_robot = robot_user.user.name

                            the_player = {"Player": user_of_the_robot, "Robot_name": robot_name}
                            list_of_players.append(the_player)


                    json_players = {"Creator": match_creator, "Players": list_of_players}
                    await websocket.send_json(json_players) 
            
                except:
                    pass
                    break

            #Una vez que se recibe que inicio la partida
            # EJERCUTAR PARTIDA
            # ENVIAR RESULTADOS DE PARTIDA
            #RESULTADOS = resultados partida
            #await websocket.send_json(RESULTADOS)




##################################################################

# IDEA DE COMO RECIBIR Y MANDAR EL JSON 

# Espero recibir:

# {
#     "id": id
# }



# IDEA DE COMO MANDAR EL JSON
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

# 1) Se podria recibir un booleano que indique si el creador ha dado al boton de iniciar partida
#  y hacer un while sobre ese booleano mientras sea falso, y salir del while una vez que sea verdadero, o cuando
#se llegue al maximo de jugadores
#  Con esto podriamos correr la partida y enviar un json con el resultado



#####################################################################
#       FUNCION PARA PRUEBAS CON DATOS FALSOS:



# @router.websocket("/") #falta agregar ruta de la funcion
# async def webssocket_endpoint_match(websocket: WebSocket):
#         print("Accepting connection")
#         await websocket.accept()
#         print("Accepted")

#         await_data = await websocket.receive_json() #recieve.text() 
#         match_id = await_data["id"]
#         #list_of_players = []
#         robot_of_the_cretor_id = 0

#         CONTADOR = 0
#         with db_session:
#             while (CONTADOR<10000):
#                 try: 
#                    while (CONTADOR<10000):
#                     list_of_players = []
#                     if CONTADOR >= 0:
#                         match_creator = {"Owner": "Jairo", "Robot_name": "Z"}


#                     if CONTADOR >= 2000:
#                         the_player = {"Player": "Jaimito", "Robot_name": "A"}
#                         list_of_players.append(the_player)

#                     if CONTADOR >= 6000:
#                         the_player = {"Player": "Pedrito", "Robot_name": "B"}
#                         list_of_players.append(the_player)

#                     if CONTADOR >= 9000:
#                         the_player = {"Player": "Tomasito", "Robot_name": "C"}
#                         list_of_players.append(the_player)

#                     json_players = {"Creator": match_creator, "Players": list_of_players}
#                     await websocket.send_json(json_players) 
            
#                 except:
#                     pass
#                     break
