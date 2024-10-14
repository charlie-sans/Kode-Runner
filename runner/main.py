import asyncio
import os
import subprocess
import sys
import tempfile
import json
from config import config
import PMS
import secure_authentication

try:
    import websockets
except ImportError:
    print("Websockets not installed. Running 'pip install websockets' to install it")
    os.system("pip install websockets")
    import websockets

import pexpect
import PMS
from debug import de_bug, debug

# Constants
DEFAULT_PASSWORD = ""
WS_PATHS = {
    "/PMS": "PMS",
    "/code": "Write_code_Buffer",
    "/PythonLSP": "PythonLSP",
    "/debug": "_debug_socket",
    "/stop": "stop_current_process"
}

# Global variables
main_Vars = {"running_programs": []}
_configs = {}

# Configuration
conf = config()
_configs["passwd"] = conf.passwd
password = conf.passwd

# Ensure directory exists
if not os.path.exists(conf.DIRECTORY):
    os.makedirs(conf.DIRECTORY)
os.chdir(conf.DIRECTORY)

# Parse command-line arguments
def parse_arguments():
    global password
    if len(sys.argv) > 1:
        skip_next = False
        for idx, arg in enumerate(sys.argv[1:]):
            if skip_next:
                skip_next = False
                continue
            match arg:
                case "-p" | "--password":
                    password = sys.argv[idx + 2]
                    skip_next = True
                case _:
                    print("Unknown argument", arg)

parse_arguments()

# Analyze code using Pyright
async def analyze_code(code):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
        tmp_path = tmp.name
        tmp.write(code.encode('utf-8'))
        tmp.flush()
        
        result = subprocess.run(['pyright', tmp_path, '--outputjson'], capture_output=True, text=True)
        os.unlink(tmp_path)
        
        if result.stdout:
            output = json.loads(result.stdout)
            diagnostics = output.get('generalDiagnostics', [])
            return json.dumps(diagnostics)
        else:
            return json.dumps({'Success': 'No output from pyright'})

# WebSocket handlers
async def PythonLSP(websocket, path):
    async for message in websocket:
        code = message
        diagnostics = await analyze_code(code)
        await websocket.send(diagnostics)

async def handler(websocket, path):
    print(websocket, path)
    match path:
        case "/PMS":
            await PMS.PMS(websocket, path)
        case "/code":
            await PMS.Write_code_Buffer(websocket, path)
        case "/PythonLSP":
            await PythonLSP(websocket, path)
        case _:
            await websocket.send("Invalid path")

# Start WebSocket server
async def start_server():
    ws_server = websockets.serve(handler, conf.WS_HOST, conf.WS_PORT)
    print("CodeRunner Server version 2.2")
    # print("TEST SERVER: Things may break")
    print("Server started at port", conf.WS_PORT)
    print("Relay started at address ws://localhost:5000/")
    if password:
        print("Using password authentication\nPassword:", repr(password))
    print("Press Ctrl+C to stop the server")
    if password:
        import threading
        print(f"\nAuth Proxy Starting at ws://{conf.passwd_proxy_host}:{conf.passwd_proxy_port}/")
        threading.Thread(target=secure_authentication.main, args=(f"ws://localhost:{conf.WS_PORT}", password)).start()
    await ws_server

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_server())
    asyncio.get_event_loop().run_forever()
