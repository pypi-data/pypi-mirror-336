import asyncio
import websockets
import json
from typing import Callable, Optional

class WebSocketServer:
    def __init__(self, host: str = "localhost", port: int = 8880):
        self.host = host
        self.port = port
        self.server = None
        self.custom_handler: Optional[Callable] = None

    async def _default_handler(self, websocket: websockets.WebSocketServerProtocol):
        """默认处理逻辑，可被自定义逻辑替代"""
        try:
            while websocket.open:
                data = await websocket.recv()
                request = json.loads(data)
                print(f"Received request: {request}")
                response = {"status": "success", "message": f"Processed: {request['data']}"}
                await websocket.send(json.dumps(response))
        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected.")

    def set_handler(self, handler: Callable[[dict, websockets.WebSocketServerProtocol], None]):
        """设置用户自定义的 WebSocket 处理逻辑"""
        self.custom_handler = handler

    async def _handler(self, websocket: websockets.WebSocketServerProtocol, path: str):
        try:
            while websocket.open:
                data = json.loads(await websocket.recv())
                if self.custom_handler:
                    await self.custom_handler(data, websocket)  # 执行用户自定义逻辑
                else:
                    await self._default_handler(websocket)  # 运行默认逻辑
        except Exception as e:
            print(f"Error: {e}")

    async def start(self):
        """启动 WebSocket 服务器"""
        self.server = await websockets.serve(self._handler, self.host, self.port)
        print(f"WebSocket server started on ws://{self.host}:{self.port}")
        await self.server.wait_closed()  # 使服务器保持运行

    def run(self):
        """运行 WebSocket 服务器，确保事件循环安全"""
        try:
            asyncio.get_running_loop()
            # 如果有运行中的事件循环，使用 `asyncio.create_task()`
            print("Detected running event loop, using create_task")
            asyncio.create_task(self.start())
        except RuntimeError:
            # 否则直接运行 `asyncio.run()`
            asyncio.run(self.start())
