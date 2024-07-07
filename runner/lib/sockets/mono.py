import os
import pexpect
import websockets
from sockets.termc import translate_terminal_colors
from sockets.debug.debug import de_bug

TEMP_PYTHON_FILE = "temp.cs"
command = "csc temp.cs"
async def execute_code(code, websocket):
    de_bug(websocket, "Executing C# code", "INFO")
    with open(TEMP_PYTHON_FILE, 'w') as file:
        file.write(code)
    child = pexpect.spawn("mono temp.exe", encoding="utf-8")
    while True:
        try:
            index = child.expect(['\n', '.', pexpect.EOF, pexpect.TIMEOUT], timeout=1)
            if index == 0 or index == 1:
                await websocket.send(child.after)
            elif index == 2:
                break
        except pexpect.exceptions.TIMEOUT as e:
            de_bug(websocket, f"Execution timed out {e}", "ERROR")
            break
    os.remove(TEMP_PYTHON_FILE)

async def Write_MONO(code, websocket):
    de_bug(websocket, "Writing C# code", "INFO")
    with open(TEMP_PYTHON_FILE, 'w') as file:
        file.write(code)
    child = pexpect.spawn(command, encoding="utf-8")
    while True:
        try:
            index = child.expect(['\n', pexpect.EOF, pexpect.TIMEOUT], timeout=1)
            if index == 0:
                await websocket.send(child.before)
            elif index == 1:
                await websocket.send(child.before)
                break
        except pexpect.exceptions.TIMEOUT as e:
            de_bug(websocket, f"Compilation timed out: {e}", "ERROR")
            break
    os.remove(TEMP_PYTHON_FILE)
    await execute_code(code, websocket)

async def MONO(websocket, path):
    
    try:
        async for code in websocket:
            await Write_MONO(code, websocket)
    except websockets.exceptions.ConnectionClosedOK as e:
        de_bug(websocket, f"Connection closed: {e}", "ERROR")
        pass