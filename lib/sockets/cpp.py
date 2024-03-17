import asyncio
import websockets
import pexpect
import os
from sockets.termc import translate_terminal_colors
TEMP_CPP_FILE = "stuff.cpp"
### START
async def execute_CPP(code, websocket):
    with open(TEMP_CPP_FILE, 'w') as file:
        file.write(code)
    os.system("g++ " + TEMP_CPP_FILE + " -o temp")
    child = pexpect.spawn(f"./temp", encoding="utf-8")

    while True:
        try:
            index = child.expect(['\n', pexpect.EOF, pexpect.TIMEOUT], timeout=1)
            if index == 0:
                
                await websocket.send(child.before)
            elif index == 1:
                
                await websocket.send(child.before)
                break
        except pexpect.exceptions.TIMEOUT:
            break
    os.remove(TEMP_CPP_FILE)

async def CPP(websocket, path):
    try:
        
        async for code in websocket:
            await execute_CPP(code, websocket)
    except websockets.exceptions.ConnectionClosedOK:
        pass
#### END