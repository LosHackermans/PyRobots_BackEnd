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

router = APIRouter()

class signUpModel(BaseModel):
    username: str
    email: str
    password: str
    # avatar: Optional[str]

    class Config:
        schema_extra = {
            'example': {
                "username": "Juan",
                "email": "juanperez@gmail.com",
                "password": "password"
            }
        }


@router.post('/create_user')
async def signup(user: signUpModel):
    with db_session:
        usernameQuery = select(
            e.username for e in User if (e.username == user.username))
        if len(usernameQuery) > 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User with this username already exists")
        emailQuery = select(e.email for e in User if (e.email == user.email))
        if len(emailQuery) > 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User with this email already exists")
        if len(user.password) < 8:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="The password must have a minimum of 8 characters")
        # if user.password != user.passwordRepeated:
            # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            # detail= "Passwords do not match")

        User(
            username=user.username,
            email=user.email,
            password=user.password,
            is_validated=False
        )

    return {"message": "User created successfully"}

@router.get('/')
def read_root():
    return {"msg": "Bienvenido de nuevo!!!"}
