import os
import pexpect
import websockets
from evall import EVAL
from sockets.termc import translate_terminal_colors
TEMP_NODE_FILE = "temp.lua"
### START
async def execute_NODE(code, websocket):
    with open(TEMP_NODE_FILE, 'w') as file:
        file.write(code)
    if EVAL(code) == False:
        
        child = pexpect.spawn(f"lua {TEMP_NODE_FILE}", encoding="utf-8")

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
        os.remove(TEMP_NODE_FILE)

async def LUA(websocket, path):
    try:
        async for code in websocket:
            await execute_NODE(code, websocket)
    except websockets.exceptions.ConnectionClosedOK:
        pass
#### END
