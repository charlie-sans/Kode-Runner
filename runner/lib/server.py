import asyncio
import os
from config import config
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

from sockets.debug.debug import de_bug
import PMSSystem.PMSsystem as PMSsystem
from sockets.go import GO
from sockets.js import NODE
from sockets.cpp import CPP
from sockets.py import server
from sockets.shell import shell
from sockets.debug import debug
from sockets.lua import LUA
from sockets.mono import MONO
conf = config()

if not os.path.exists(conf.DIRECTORY):
    os.makedirs(conf.DIRECTORY)
    
os.chdir(conf.DIRECTORY)

async def handler(websocket, path):
    print(websocket, path)
    match path:
        case "/lang":
            pass
        case "/js":
            await NODE(websocket, path)
        case "/go":
            await GO(websocket, path)
        case "/cpp":
            await CPP(websocket, path)
        case "/lua":
            await LUA(websocket, path)
        case "/mono":
            await MONO(websocket, path)
        
        case "/help":
            await websocket.send(conf.help)
        case "/test":
            websocket.send("starting test")
            data = PMSsystem.PMSSystem.assign(await websocket.recv())
            print(data)
            await websocket.send(data)
        case "/PMS":
            await PMSsystem.PMSSystem.PMSSystemStartup(websocket, path)
        case "/code":
            await PMSsystem.PMSSystem.PMSCode(websocket, path)
        case "/py":
            await server(websocket, path)
        case "/shell":
            de_bug("Connected to shell server", "INFO")
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
        case "/request": await websocket.send(conf.endpoints)
        case _: await websocket.send("Invalid path")



ws_server = websockets.serve(handler, conf.WS_HOST, conf.WS_PORT)

print("CodeRunner Server version 2.0")
print("TEST SERVER: Things may break")
print("Server started at port", conf.WS_PORT)
print("Relay started at address https://localhost:5000/")
print("Press Ctrl+C to stop the server")
asyncio.get_event_loop().run_until_complete(ws_server)

asyncio.get_event_loop().run_forever()