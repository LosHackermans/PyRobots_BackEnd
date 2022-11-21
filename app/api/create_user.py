
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.api.models import *
from pony.orm import db_session
from fastapi import APIRouter
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
import random
import os
from app.api.upload_robot import Body
from robots.default_robots.CircleBot import CircleBot
from robots.default_robots.SquareBot import SquareBot
from app.api.upload_robot import update_default_robot

conf = ConnectionConfig(
    MAIL_USERNAME = "pyrobotsok@gmail.com",
    MAIL_PASSWORD = "qxdevnpfcerygkqp",
    MAIL_FROM = "pyrobotsok@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Verification Code",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

router = APIRouter()


class signUpModel(BaseModel):
    username: str
    email: str
    password: str
    avatar: str

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


        verify_token = ''.join(random.choice('0123456789ABCDEF') for i in range(7))
        
        html = f"""<p>Hi,thanks for signing up for pyrobots! Your verification code is: {verify_token} </p>
                  <p> http://localhost:3000/verify_user </p>"""
        email_s1 = EmailStr(user.email)
        list_emails =[]
        list_emails.append(email_s1)
        message = MessageSchema(
            subject="Fastapi-Mail module",
            recipients=list_emails,
            body=html,
            subtype=MessageType.html)


        current_user = User(
            username=user.username,
            email=user.email,
            password=user.password,
            avatar=user.avatar,
            is_validated=False,
            verify_token = verify_token
        )
        
        fm = FastMail(conf)
        await fm.send_message(message)

        # Upload default robots
        update_default_robot(CircleBot, current_user)
        update_default_robot(SquareBot, current_user)

        return {"message": "User created successfully"}
