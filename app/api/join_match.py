from email.headerregistry import ParameterizedMIMEHeader
from functools import partialmethod
from importlib.metadata import requires
from unicodedata import name
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import jwt
from pydantic import BaseModel
import base64
from app.api.models import *
from fastapi.encoders import jsonable_encoder
from typing import Optional
import json
from pony.orm import db_session
from fastapi import APIRouter



# TODO: 

# - Tarea
#       - Los datos del front que intesan son solo el name y password de sala, y el los datos del usuario
#       - El usuario ve las partidas a las que se puede unir
#       - Verificar si se puede unir a la partida (is_joinable), pero puede ser que no haga falta
#       - Luego si es joinable, agregar al usuario a la partida
#       - Luego verificar si la cantidad de jugadores en la partida super la max_players, si pasa cambiar joinable a False




# Preguntas:
#     - El front envia el name o el id, el front tiene acceso al id, preguntar al que se encarga de la parte de listar partidas, y en el front cuando la seleccionas??
#     - Preguntar que pasa si dos usuarios al mismo tiempo intentan unirse o si es posible que eso pase
#          - Por el tema de verificar si es joinable

# id_match: str
# or
# name_match=body.name, 

# password=body.password,

# user=curent_user (user id o username)

router = APIRouter()


# NOTE: The BaseModel fails if user not created
class JoinMatchModel(BaseModel): 
    id_match: int # El front puede enviar id? El nombre y demas puede repetirse
    password_match: str
    username: str

    class Config:
        schema_extra = {
            'example': {
                "id_match": 1,
                "password_match": "testPassword",
                "username": "testUser"
            }
        }


@router.post('/join_match')
async def join_match(match: JoinMatchModel):
 
    with db_session:
        # Primero busco el match en la bd para extraer los datos, sobre todo si es joinable
        current_match = Match.get(id=match.id_match)
        current_user = User.get(username=match.username) # Por ahora dejarlo asi, ver como se recibe al usuario
        # si se pudo unir es porq el match existe
        if current_match == None: # Ver si esto puede pasar
            pass # El match no exist ?
        if (current_user == None):
            pass # No existe Usuario? 
        if (current_match.password != match.password_match):
            pass # Password incorrecta

        # TODO: Agregar a Match el usuario


    return {"message": "User add successfully"}
