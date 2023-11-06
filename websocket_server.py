import asyncio
import time
import json
from websockets import serve
from utils.serverutils import ServerManager


class SocketServer:
    def __init__(self, host: str, port: int, server_manager: ServerManager):
        self.host = host
        self.port = port
        self.server_manager = server_manager

    async def handler(self, websocket):
        self.websocket = websocket
        while True:
            try:
                message = await websocket.recv()
                print(message)

                status_update = {
                    "type": "status_update",
                    "server_status": self.server_manager.status,
                }
                await websocket.send(json.dumps(status_update))
            except Exception as e:
                print(e)

    async def start_server(self):
        print("STARTING SERVER")
        async with serve(self.handler, self.host, self.port):
            await asyncio.Future()

    async def update_status(self, status):
        while True:
            await self.websocket.send(status)
            time.sleep(5000)

    def run(self):
        print("STARTING SERVER")
        asyncio.run(self.start_server())
