from fastapi import FastAPI, Request
import jwt
from pydantic import BaseModel
from app.api.models import *
from fastapi.encoders import jsonable_encoder
from pony.orm import db_session
from fastapi import APIRouter
from app.get_user import SECRET_KEY, ALGORITHM

router = APIRouter()

class LoginItem(BaseModel):
    email: str
    password: str


@router.post("/login")
async def login_user(login_item: LoginItem):
    data = jsonable_encoder(login_item)
    with db_session:
        if User.exists(email=data["email"]):
            currentUser = User.get(lambda u: u.email == data["email"])
            if not currentUser.is_validated:
                return {'error': ' not verify'}
            if currentUser.password == data["password"] :
                encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
                return {'token': encoded_jwt}
            else:
                return {'error': ' incorrect Password'}
        if not(User.exists(email=data["email"])):
            return {'error': 'User not exist'}

