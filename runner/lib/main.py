import asyncio
import os
from config import config
try:
    import websockets
except ImportError:
    print("Websockets not installed. Running 'pip install websockets' to install it")
    os.system("pip install websockets")
    import websockets
import pexpect
import subprocess
import re
import sys

from sockets.debug.debug import de_bug
import PMSSystem.PMSsystem as PMSsystem


from sockets.cpp import CPP
from sockets.py import server

from sockets.debug import debug

import passwd_handler

conf = config()

if not os.path.exists(conf.DIRECTORY):
    os.makedirs(conf.DIRECTORY)
    
os.chdir(conf.DIRECTORY)

if len(sys.argv) > 1:
    skip_next = False
    for idx, i in enumerate(sys.argv[1:]):
        if skip_next == True:
            skip_next = False
            continue
        match i:
            case "-p":
                passwd_handler.set_password(sys.argv[idx+2])
                skip_next = True
            case "--password":
                passwd_handler.set_password(sys.argv[idx+2])
                skip_next = True
            case _:
                print("Unknown argument", i)


async def analyze_code(code):
    # Write code to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
        tmp_path = tmp.name
        tmp.write(code.encode('utf-8'))
        tmp.flush()
        
        # Run pyright as a subprocess
        result = subprocess.run(['pyright', tmp_path, '--outputjson'], capture_output=True, text=True)
        
        # Delete the temporary file
        os.unlink(tmp_path)
        
        # Parse pyright's JSON output
        if result.stdout:
            output = json.loads(result.stdout)
            diagnostics = output.get('generalDiagnostics', [])
            return json.dumps(diagnostics)
        else:
            return json.dumps({'Success': 'No output from pyright'})

async def PythonLSP(websocket, path):
    async for message in websocket:
        code = message
        diagnostics = await analyze_code(code)
        await websocket.send(diagnostics)



async def handler(websocket, path):
    print(websocket, path)
    match path:
        case "/PYLSP":
            await PythonLSP(websocket, path)
        case "/cpp":
            await CPP(websocket, path)
        case "/py":
          await server(websocket, path)
        case "/help":
            await websocket.send(conf.help)
        case "/PMS":
            await PMSsystem.PMS(websocket, path)
        case "/code":
            await PMSsystem. Write_code_Buffer (websocket, path)
        case "/debug":
            de_bug(websocket, "Connected to debug server", "INFO")
            await debug(websocket, path)
        case "/":
            # relay all code to everyone connected
            print("relay server connected")
            while True:
                code = await websocket.recv()
                # send the received code to all connected clients
                for client in websockets:
                    await client.send(code)
                    
        case "/request": await websocket.send(conf.endpoints)
        case _: await websocket.send("Invalid path")



    
ws_server = websockets.serve(handler, conf.WS_HOST, conf.WS_PORT)
print("CodeRunner Server version 2.0")
print("TEST SERVER: Things may break")
print("Server started at port", conf.WS_PORT)
print("Relay started at address https://localhost:5000/")
if passwd_handler.has_password:
    print("Using password authentication\nPassword:", passwd_handler.get_password())
print("Press Ctrl+C to stop the server")
asyncio.get_event_loop().run_until_complete(ws_server)
asyncio.get_event_loop().run_forever()
