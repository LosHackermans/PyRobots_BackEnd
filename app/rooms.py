from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, match_id: str):
        await websocket.accept()
        if match_id not in self.active_connections:
            self.active_connections[match_id] = [websocket]
        else:
            self.active_connections[match_id].append(websocket)

    async def disconnect(self, websocket: WebSocket, match_id: str):
        self.active_connections[match_id].remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: str, match_id: str):
        for connection in self.active_connections[match_id]:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(e)
