import asyncio
import websockets
import json

class WebSocketClient:
    def __init__(self, websocket_url: str, timeout: int = 10):
        self.websocket_url = websocket_url  # WebSocket 连接地址
        self.timeout = timeout  # 连接超时时间
        self.websocket = None  # WebSocket 连接
        self.connected_event = asyncio.Event()  # 事件用于标记 WebSocket 连接成功
        asyncio.create_task(self.init_websocket())  # 在后台任务中初始化 WebSocket

    async def init_websocket(self):
        """初始化 WebSocket 连接"""
        try:
            self.websocket = await websockets.connect(self.websocket_url, timeout=self.timeout)
            print("WebSocket connection established.")
            self.connected_event.set()  # 标记连接已建立
            
        except Exception as e:
            print(f"WebSocket connection failed: {e}")

    async def send_request(self, data):
        """发送请求并接收响应"""
        await self.connected_event.wait()  # 等待 WebSocket 连接建立
        if self.websocket is None or self.websocket.closed:
            print("WebSocket is not connected or already closed!")
            return

        try:
            # 发送请求数据
            await self.websocket.send(json.dumps(data))
            print(f"Sent request: {data}")

            # 接收并返回服务器响应
            response = await self.websocket.recv()
            print(f"Received response: {response}")
            return response
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection was closed unexpectedly.")

    async def close_websocket(self):
        """关闭 WebSocket 连接"""
        if self.websocket:
            await self.websocket.close()
            print("WebSocket connection closed.")
