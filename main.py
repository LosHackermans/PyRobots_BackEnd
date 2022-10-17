from fastapi import FastAPI
from userRouter import router as userRouter
from models import db


app = FastAPI()
app.include_router(userRouter)
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)


@app.get("/")
async def root():
    return {"message": "Hello World"}
