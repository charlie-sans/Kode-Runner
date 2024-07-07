import websockets
import pexpect
import os

from sockets.termc import convert_string_to_color_code
TEMP_BASH_FILE = "temp.sh"


### START
async def execute_shell(code, websocket):
    with open(TEMP_BASH_FILE, 'w') as file:
        file.write(code)
    
    child = pexpect.spawn(f"/bin/bash {TEMP_BASH_FILE}", encoding="utf-8")

    while True:
        try:
            index = child.expect(['\n', '.', pexpect.EOF, pexpect.TIMEOUT], timeout=1)
            if index == 0 or index == 1:
                #coded_text = translate_terminal_colors(child.before)
                await websocket.send(child.after)
            elif index == 2:
                break
        except pexpect.exceptions.TIMEOUT:
            break
    os.remove(TEMP_BASH_FILE)

async def shell(websocket, path):
    try:
        async for code in websocket:
            await execute_shell(code, websocket)
    except websockets.exceptions.ConnectionClosedOK:
        pass
#### END

    