import email
from re import A
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import jwt
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, FastAPI

# Se importa la base de datos
from models import *

# TODO: put some of this in .env file
ACCESS_TOKEN_EXPIRE_MINUTES = 800
FRONTEND_URL = "http://localhost:3001"

app = FastAPI()


# lo que deberia pasarme
test_user = {
    "number_of_rounds": 200,
    "number_of_games": 100,
    "min_players": 2,
    "max_players": 4,
    "token": "abc",
}

origins = {
    "http://localhost",
    FRONTEND_URL,
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
def fake_decode_token(token):
    return User(username=token + "fakedecoded", email="john@example.com",
                password="John Doe")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    a: User
    a = fake_decode_token(token)
    return a
"""

@app.get("/")
def read_root():
    return {"Bienvenido de nuevo!!!"}


@app.post("/creatematch")
async def user_creatematch():
    with db_session:
        Match(id=1, name="ejmplo", min_players="min_players",
        max_players="max_players", number_rounds="number_rounds", number_games="number_games",
        user=User.select(lambda u: u.id), robot_in_matches="?")
        commit()
    return {"message": "the match was created successfully"}
