from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections= []

    async def connect(self, websocket: WebSocket, match_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket, match_id: str):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(e)