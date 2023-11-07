import asyncio
import json
import logging
from websockets import serve
from utils.serverutils import ServerManager


class SocketServer:
    def __init__(self, host: str, port: int, server_manager: ServerManager):
        self.host = host
        self.port = port
        self.server_manager = server_manager

    async def handler(self, websocket):
        self.websocket = websocket
        try:
            message = await websocket.recv()
            # print(message)

            status_update = {
                "type": "status_update",
                "server_status": self.server_manager.status,
                "connected_players": self.server_manager.connected_players,
            }

            await websocket.send(json.dumps(status_update))
        except Exception as e:
            pass
            # print(e)

    async def start_server(self):
        print("STARTING SERVER")
        logging.getLogger("websockets").setLevel(logging.ERROR)
        async with serve(self.handler, self.host, self.port):
            await asyncio.Future()

    def run(self):
        print("STARTING SERVER")
        asyncio.run(self.start_server())
