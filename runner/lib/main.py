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

from debug import de_bug
import PMSsystem

from debug import debug

import auth_proxy

conf = config()

password = conf.passwd

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
                password = sys.argv[idx+2]
                skip_next = True
            case "--password":
                password = sys.argv[idx+2]
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
        
        case "/PMS":
            await PMSsystem.PMS(websocket, path)
        case "/code":
            await PMSsystem. Write_code_Buffer (websocket, path)
        
        case _: await websocket.send("Invalid path")



    
ws_server = websockets.serve(handler, conf.WS_HOST, conf.WS_PORT)
print("CodeRunner Server version 2.0")
print("TEST SERVER: Things may break")
print("Server started at port", conf.WS_PORT)
print("Relay started at address ws://localhost:5000/")
if password != "":
    print("Using password authentication\nPassword:", repr(password))
print("Press Ctrl+C to stop the server")
if password != "":
    import threading # I am definitly **Not** putting this here because I am too lazy to go to the top of the file. - Carson Coder
    print(f"\nAuth Proxy Starting at ws://{conf.passwd_proxy_host}:{conf.passwd_proxy_port}/")
    threading.Thread(target=auth_proxy.main, args=(f"ws://localhost:{conf.WS_PORT}",password)).start()
asyncio.get_event_loop().run_until_complete(ws_server)
asyncio.get_event_loop().run_forever()
