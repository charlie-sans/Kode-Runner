import asyncio
import websockets
import pexpect
import os
from sockets.debug.debug import de_bug
from sockets.termc import translate_terminal_colors
TEMP_CPP_FILE = "temp.cpp"
async def execute_CPP( websocket):
    de_bug(websocket, "Executing C++ code", "INFO")
    if not os.path.exists("./temp"):
        print("Executable file not found, halting execution")
        de_bug(websocket, "Executable file not found, did you forget to change the language when running other code?", "ERROR")
        return
    child = pexpect.spawn(f"./temp", encoding="utf-8")

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
        except pexpect.exceptions.TIMEOUT as e:
            de_bug(websocket, f"Execution timed out {e}", "ERROR")
            break
   
 
async def write_CPP(code, websocket):
    de_bug(websocket, "Writing C++ code", "INFO")
    with open(TEMP_CPP_FILE, 'w') as file:
        file.write(code)

    child = pexpect.spawn(f"g++ {TEMP_CPP_FILE} -o temp", encoding="utf-8")

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
        except pexpect.exceptions.TIMEOUT as e:
            de_bug(websocket, f"Compilation timed out: {e}", "ERROR")
            break
    os.remove(TEMP_CPP_FILE)
    await execute_CPP(websocket)

async def CPP(websocket, path):
    try:

        async for code in websocket:
            await write_CPP(code, websocket)
    except websockets.exceptions.ConnectionClosedOK as e:
        await de_bug(websocket, f"Connection closed: {e}", "ERROR")
        pass
#### END