import asyncio
from websockets.asyncio.client import connect
from websockets.asyncio.server import serve
import websockets
import time
import config

global password
global ws_url
ws_url = ""
password = ""

conf = config.config()

async def ctos(client, server):
    while True:
        msg = await client.recv()
        print("Client:", msg)
        await server.send(msg)

async def stoc(client, server):
    while True:
        msg = await server.recv()
        print("Server:", msg)
        await client.send(msg)

async def client(socket, url):
    websocketurl = ws_url + url
    
    await socket.send("[password]")
    passwd = await socket.recv()
    print("\nConnection request attempt with password:", repr(passwd))
    
    if str(passwd) != str(password):
        await socket.send("[wrong]")
        print("recived incorrect password")
        await socket.close()
        return
    else:
        print("Correct password")
        await socket.send("[correct]")
    
    async with connect(websocketurl) as websocket:
        await asyncio.gather(
            ctos(socket, websocket),
            stoc(socket, websocket),
        )

async def server():
    async with websockets.serve(client, conf.passwd_proxy_host, conf.passwd_proxy_port):
        await asyncio.get_running_loop().create_future()  # run forever

def main(websocket_url, passwd):
    global ws_url
    global password
    password = passwd
    ws_url = websocket_url
    asyncio.run(server())

if __name__ == "__main__":
    main("ws://localhost:5000/", "hi")
