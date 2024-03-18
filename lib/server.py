import asyncio
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


WS_HOST = "127.0.0.1"
WS_PORT = 5000


SHELL = "/bin/bash"
TEMP_PYTHON_FILE = "code/temp.py"
TEMP_BASH_FILE = "code/temp.sh"
TEMP_CPP_FILE = "code/temp.cpp"
TEMP_NODE_FILE = "code/temp.js"
TEMP_GO_FILE = "code/temp.go"

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
        print("python")
        await server(websocket, path)
    else:
        await websocket.send("Invalid path")

    



ws_server = websockets.serve(handler, WS_HOST, WS_PORT)



print("Server started at port", WS_PORT)
print("Shell started at address https://localhost:5000/shell")
print("Node started at address https://localhost:5000/node")
print("C++ started at address https://localhost:5000/cpp")
print("Go started at address https://localhost:5000/go")
print("Python started at address https://localhost:5000/py")


asyncio.get_event_loop().run_until_complete(ws_server)

asyncio.get_event_loop().run_forever()