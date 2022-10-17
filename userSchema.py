from pydantic import BaseModel
from typing import Optional

class signUpModel(BaseModel):
    username: str
    email: str
    password: str 
    # avatar = Optional[str]

    class Config:
        schema_extra = {
            'example':{
                "username": "Juan",
                "email": "juanperez@gmail.com",
                "password": "password",
                "is_validated": False
            }
        }