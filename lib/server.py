import asyncio
import websockets
import pexpect
import os
import subprocess
import re

WS_HOST = "127.0.0.1"
WS_PORT = 5000
ws_port2 = 5001
ws_port3 = 5002
ws_port4 = 5003
ws_port5 = 5004
ws_port6 = 5005
ws_port7 = 5006
ws_port8 = 5007
ws_port9 = 5008
ws_port10 = 5009

SHELL = "/bin/bash"
TEMP_PYTHON_FILE = "code/temp.py"
TEMP_BASH_FILE = "code/temp.sh"
TEMP_CPP_FILE = "code/temp.cpp"
TEMP_NODE_FILE = "code/temp.js"
TEMP_GO_FILE = "code/temp.go"

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
        '7': 'white',
        '8': 'black',
        '9': 'red',
        '10': 'green',
        '11': 'yellow',
        '12': 'blue',
        '13': 'magenta',
        '14': 'cyan',
        '15': 'white',
        '9': 'red',
        '10': 'green',
        '11': 'yellow',
        '12': 'blue',
        '13': 'magenta',
        '14': 'cyan',
        '15': 'white',
        '30': 'black',
        '31': 'red',
        '32': 'green',
        '33': 'yellow',
        '34': 'blue',
        '35': 'magenta',
        '36': 'cyan',
        '37': 'white',
        '100': 'black',
        '101': 'red',
        '110': 'green',
        '111': 'yellow',
        '112': 'blue',
        '113': 'magenta',
        '114': 'cyan',
        '115': 'white',
        '40': 'black',
        '41': 'red',
        '42': 'green',
        '43': 'yellow',
        '44': 'blue',
        '45': 'magenta',
        '46': 'cyan',
        '47': 'white',
        '100': 'black',
        '101': 'red',
        '102': 'green',
        '103': 'yellow',
        '104': 'blue',
        '105': 'magenta',
        '106': 'cyan',
        '107': 'white',
        '108': 'black'
    
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
### START
async def execute_CPP(code, websocket):
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
### START
async def execute_NODE(code, websocket):
    with open(TEMP_NODE_FILE, 'w') as file:
        file.write(code)
    
    child = pexpect.spawn(f"node {TEMP_NODE_FILE}", encoding="utf-8")

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

async def NODE(websocket, path):
    try:
        async for code in websocket:
            await execute_NODE(code, websocket)
    except websockets.exceptions.ConnectionClosedOK:
        pass
#### END
### START
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
#### END

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
ws_node = websockets.serve(NODE, WS_HOST, ws_port3)
ws_cpp = websockets.serve(CPP, WS_HOST, ws_port4)
ws_go = websockets.serve(GO, WS_HOST, ws_port5)


print("Server started at port", WS_PORT)
print("Shell started at port", ws_port2)
print("Node started at port", ws_port3)
print("C++ started at port", ws_port4)
print("Go started at port", ws_port5)
asyncio.get_event_loop().run_until_complete(ws_go)
asyncio.get_event_loop().run_until_complete(ws_shell)
asyncio.get_event_loop().run_until_complete(ws_server)
asyncio.get_event_loop().run_until_complete(ws_node)
asyncio.get_event_loop().run_until_complete(ws_cpp)
asyncio.get_event_loop().run_forever()