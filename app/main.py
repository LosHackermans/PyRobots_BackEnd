from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import login, create_match, create_user, upload_robot, list_robots, list_matches, join_match, create_simulation, lobby, web_socket_lobby
from app.api import remove_player, get_profile


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router)
app.include_router(create_user.router)
app.include_router(create_match.router)
app.include_router(upload_robot.router)
app.include_router(create_simulation.router)
app.include_router(join_match.router)
app.include_router(list_robots.router)
app.include_router(list_matches.router)
app.include_router(web_socket_lobby.router)
app.include_router(lobby.router)
app.include_router(remove_player.router)
app.include_router(get_profile.router)