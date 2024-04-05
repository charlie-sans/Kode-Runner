import asyncio
import websockets
import pexpect
import os
from sockets.termc import translate_terminal_colors
TEMP_GO_FILE = "/code/temp.go"

### START
async def execute_GO(code, websocket):
    with open(TEMP_GO_FILE, 'w') as file:
        file.write(code)
    
    child = pexpect.spawn(f"g++ {TEMP_GO_FILE} -o temp", encoding="utf-8")

    while True:
        try:
            index = child.expect(['\n', pexpect.EOF, pexpect.TIMEOUT], timeout=1)
            if index == 0:
                coded_text = translate_terminal_colors(child.before)
                await websocket.send(coded_text)
            elif index == 1:
                coded_text = translate_terminal_colors(child.before)
                await websocket.send(coded_text)
                break
        except pexpect.exceptions.TIMEOUT:
            break
    os.remove(TEMP_GO_FILE)

async def GO(websocket, path):
    try:
        
        async for code in websocket:
            await execute_GO(code, websocket)
    except websockets.exceptions.ConnectionClosedOK:
        pass
#### END