from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class LoginItem(BaseModel):
    email: str
    password: str
@app.get("/")
def read_root():
    return {"Hello": "World"}
@app.post("/login")
async def login_user(login_item: LoginItem):
    return login_item