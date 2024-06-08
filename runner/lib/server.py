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
from sockets.debug.debug import de_bug
import re
from sockets.go import GO
from sockets.js import NODE
from sockets.cpp import CPP
from sockets.py import server
from sockets.shell import shell
from sockets.debug import debug
from sockets.lua import LUA
from sockets.mono import MONO
endpoints = ["ws://localhost:5000/mono,","ws://localhost:5000/js,","ws://localhost:5000/py,","ws://localhost:5000/cpp,","ws://localhost:5000/lua,","ws://localhost:5000/shell,"]
WS_HOST = "0.0.0.0"
WS_PORT = 5000



DIRECTORY= "code"
if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)

async def handler(websocket, path):
    match path:
        case "/mono":
            de_bug(websocket, "Connected to mono server", "INFO")
            await MONO(websocket, path)
        case "/cpp":
            de_bug(websocket, "Connected to cpp server", "INFO")
            await CPP(websocket, path)
        case "/py":
            de_bug(websocket, "Connected to python server", "INFO")
            await server(websocket, path)
        case "/js":
            de_bug(websocket, "Connected to node server", "INFO")
            await NODE(websocket, path)
        case "/go":
            de_bug(websocket, "Connected to go server", "INFO")
            await GO(websocket, path)
        case "/lua":
            de_bug(websocket, "Connected to lua server", "INFO")
            await LUA(websocket, path)
        case "/shell":
            de_bug(websocket, "Connected to shell server", "INFO")
            await shell(websocket, path)
        case "/debug":
            de_bug(websocket, "Connected to debug server", "INFO")
            await debug(websocket, path)
        case "/":
            # relay all code to everyone connected
            print("relay server connected")
            while True:
                code = await websocket.recv()
                # send the received code to all connected clients
                for client in websockets:
                    await client.send(code)
        case "/request":
            await websocket.send(endpoints)
        case _: await websocket.send("Invalid path")



ws_server = websockets.serve(handler, WS_HOST, WS_PORT)

print("CodeRunner Server version 2.0")
print("Server started at port", WS_PORT)
print("Relay started at address https://localhost:5000/")
print("Press Ctrl+C to stop the server")
asyncio.get_event_loop().run_until_complete(ws_server)

asyncio.get_event_loop().run_forever()