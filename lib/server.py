import asyncio
import os

try:
    import websockets
except ImportError:
    print("Websockets not installed. Running 'pip install websockets' to install it")
    os.system("pip install websockets")
    import websockets
    

import pexpect
import os
import subprocess
import re
from sockets.go import GO
from sockets.js import NODE
from sockets.cpp import CPP
from sockets.py import server
from sockets.shell import shell
from sockets.debug import debug
from sockets.mono import MONO


WS_HOST = "0.0.0.0"
WS_PORT = 5000


DIRECTORY= "code"
if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)

async def handler(websocket, path):
    if websocket.path == "/shell":
        print("bash connected")
        await shell(websocket, path)
    elif websocket.path == "/node":
        print("node connected")
        await NODE(websocket, path)
    elif websocket.path == "/cpp":
        print("cpp compiler connected")
        await CPP(websocket, path)
    elif websocket.path == "/go":
        print("go connected")
        await GO(websocket, path)
    elif websocket.path == "/py":
        print("python server connected")
        await server(websocket, path)
    elif websocket.path == "/debug":
        print("debug server connected")
        await debug(websocket, path)
    elif websocket.path == "/js":
        print("Node connected")
        await NODE(websocket, path)
    elif websocket.path == "/lua":
        print("lua connected")
        await NODE(websocket, path)
    elif websocket.path == "/mono":
        print("mono connected")
        await MONO(websocket, path)
    elif websocket.path == "/":
        # relay all code to everyone connected
        print("relay server connected")
        while True:
            code = await websocket.recv()
            # send the received code to all connected clients
            for client in websockets:
                await client.send(code)
    else:
        await websocket.send("Invalid path")


ws_server = websockets.serve(handler, WS_HOST, WS_PORT)

print("Code Runner Server version 1.0")
print("Server started at port", WS_PORT)
print("Shell started at address https://localhost:5000/shell")
print("Node started at address https://localhost:5000/node")
print("C++ started at address https://localhost:5000/cpp")
print("Go started at address https://localhost:5000/go")
print("Python started at address https://localhost:5000/py")
print("Debug started at address https://localhost:5000/debug")
print("Lua started at address https://localhost:5000/lua")
print("Mono started at address https://localhost:5000/mono")
print("Relay started at address https://localhost:5000/")
print("Press Ctrl+C to stop the server")



asyncio.get_event_loop().run_until_complete(ws_server)

asyncio.get_event_loop().run_forever()