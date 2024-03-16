import asyncio
import websockets
import pexpect
import os
import subprocess
import re

WS_HOST = "127.0.0.1"
WS_PORT = 5000
WS_HOST_PYTHON = "127.0.0.1/py"
WS_HOST_JS = "127.0.0.1/js"
WS_HOST_CPP = "127.0.0.1/cpp"
WS_HOST_GO = "127.0.0.1/go"
WS_SHELL = 5001
WS_ERROR = 5002


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

async def execute_code(code, websocket, file,command):
    try:
        with open(file, 'w') as file:
            file.write(code)
    except Exception as e:
        print(e)
        return
    child = pexpect.spawn(f"{command} {file}", encoding="utf-8")

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
    try:
        os.remove(file)
    except Exception as e:
        print(e)
        return
async def handler(websocket, path):
    if websocket.path == "/py":
        try:
            async for code in websocket:
                await execute_code(code, websocket, "code/temp.py", SHELL)
        except websockets.exceptions.ConnectionClosedOK:
            pass
    
    elif websocket.path == "/cpp":
        try:
            async for code in websocket:
                await execute_code(code, websocket, "code/temp.cpp", "g++ temp.cpp -o temp && ./temp")
        except websockets.exceptions.ConnectionClosedOK:
            pass
    elif websocket.path == "/go":
        try:
            async for code in websocket:
                await execute_code(code, websocket, "code/temp.go", "go run .")
        except websockets.exceptions.ConnectionClosedOK:
            pass
    elif websocket.path == "/":
        async for code in websocket:
            await execute_shell(code, websocket)
        

    else:
        # No handler for this path; close the connection.
        return

# Debugging handler for sending messages to the client from the server.
async def debug(websocket, path,cat):
    try:
        async for message in websocket:
            await websocket.send(message)
    except websockets.exceptions.ConnectionClosedOK:
        pass
    except Exception as e:
        print(e)
        return



# Start the server.
ws_server = websockets.serve(handler, WS_HOST, WS_PORT)
ws_debug_server = websockets.serve(debug, WS_HOST, WS_SHELL)



print("Starting server...")


print("Server started at port", WS_PORT)
print("Shell started at address ", WS_HOST_PYTHON)
print("Shell started at address ", WS_HOST_JS)
print("Shell started at address ", WS_HOST_CPP)
print("Shell started at address ", WS_HOST_GO)

asyncio.get_event_loop().run_until_complete(ws_server)

asyncio.get_event_loop().run_forever()