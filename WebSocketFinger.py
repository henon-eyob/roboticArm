import asyncio
import websockets


async def listen():
    url = "ws://192.168.143.136:8080"
    async with websockets.connect(url) as ws:
        await ws.send("hello server")

asyncio.get_event_loop().run_until_complete(listen())
