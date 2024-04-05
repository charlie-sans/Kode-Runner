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
    child = pexpect.spawn("csc temp.cs", encoding="utf-8")
    child.expect(pexpect.EOF)  # Wait for the compilation to finish
    
    await websocket.send(child.before)
    child = pexpect.spawn("mono temp.exe", encoding="utf-8")
    while True:
        try:
            index = child.expect(['\n', pexpect.EOF, pexpect.TIMEOUT], timeout=1)
            if index == 0:
                await websocket.send(child.before)
            elif index == 1:
                await websocket.send(child.before)
                break
        except pexpect.exceptions.TIMEOUT as e:
            de_bug(websocket, f"Execution timed out {e}", "ERROR")
            break
    os.remove(TEMP_PYTHON_FILE)

async def MONO(websocket, path):
    
    try:
        async for code in websocket:
            await execute_code(code, websocket)
    except websockets.exceptions.ConnectionClosedOK as e:
        de_bug(websocket, f"Connection closed: {e}", "ERROR")
        pass