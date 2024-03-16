import asyncio
import websockets
import pexpect
import os
import subprocess
import re

WS_HOST = "127.0.0.1"
WS_PORT = 5000
ws_port2 = 5001
SHELL = "/bin/bash"
TEMP_PYTHON_FILE = "temp.py"
TEMP_BASH_FILE = "temp.sh"
DIRECTORY= "code"
if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)
def translate_terminal_colors(code):
    color_mapping = {
        '0': 'black',
        '1': 'red',
        '2': 'green',
        '3': 'yellow',
        '4': 'blue',
        '5': 'magenta',
        '6': 'cyan',
        '7': 'white'
    }
    
    translated_code = ''
    i = 0
    while i < len(code):
        if code[i] == '\x1b' and code[i+1] == '[':
            j = i + 2
            while code[j].isdigit() or code[j] == ';':
                j += 1
            if code[j] == 'm':
                color_codes = code[i+2:j].split(';')
                for color_code in color_codes:
                    if color_code in color_mapping:
                        translated_code += f'<color={color_mapping[color_code]}>'
                    else:
                        translated_code += f'<color={color_code}>'
                i = j + 1
                continue
        translated_code += code[i]
        i += 1
    
    return translated_code

async def execute_shell(code, websocket):
    with open(TEMP_BASH_FILE, 'w') as file:
        file.write(code)
    
    child = pexpect.spawn(f"/bin/bash {TEMP_BASH_FILE}", encoding="utf-8")

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
    os.remove(TEMP_BASH_FILE)

async def shell(websocket, path):
    try:
        async for code in websocket:
            await execute_shell(code, websocket)
    except websockets.exceptions.ConnectionClosedOK:
        pass


async def execute_code(code, websocket):
    with open(TEMP_PYTHON_FILE, 'w') as file:
        file.write(code)
    
    child = pexpect.spawn(f"python3 {TEMP_PYTHON_FILE}", encoding="utf-8")

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
    os.remove(TEMP_PYTHON_FILE)

async def server(websocket, path):
    try:
        async for code in websocket:
            await execute_code(code, websocket)
    except websockets.exceptions.ConnectionClosedOK:
        pass


ws_server = websockets.serve(server, WS_HOST, WS_PORT)
ws_shell = websockets.serve(shell, WS_HOST, ws_port2)
print("Server started at port", WS_PORT)
print("Shell started at port", ws_port2)
asyncio.get_event_loop().run_until_complete(ws_shell)
asyncio.get_event_loop().run_until_complete(ws_server)
asyncio.get_event_loop().run_forever()