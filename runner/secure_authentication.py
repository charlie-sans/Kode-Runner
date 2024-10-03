import asyncio
from websockets.asyncio.client import connect
from websockets.asyncio.server import serve
import websockets
import time
import config
import random

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

# id: socket
recv_sockets = {}

async def client(socket, url):
    print("Connection at", url)
    websocketurl = ws_url + url
    if not url == "/recv":
        connid = await socket.recv()
        if connid in recv_sockets:
            recv_socket = recv_sockets[connid]
        else:
            await socket.send("Could not find connection_id: " + connid)
            return

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
                stoc(recv_socket, websocket),
            )
    else:
        connection_id = hex(random.randint(0,0xFFFFFFFF))
        print("Recv connection with id", connection_id)
        recv_sockets[connection_id] = socket
        await socket.send(connection_id)
        await socket.wait_closed()

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
