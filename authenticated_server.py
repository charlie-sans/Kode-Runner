import asyncio
from websockets.sync.client import connect
#from websockets.asyncio.server import serve
from websockets.server import serve

ws_url = ""

def client(websocketurl, socket):
    with connect(websocketurl) as websocket:
        for msg in socket:
            websocket.send(msg)

async def echo(websocket):
    client(ws_url, websocket)

async def server():
    async with serve(echo, "localhost", 5050):
        await asyncio.get_running_loop().create_future()  # run forever

def main(websocket_url):
    global ws_url
    ws_url = websocket_url
    asyncio.run(server())
