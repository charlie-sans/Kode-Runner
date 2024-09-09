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
import os
import subprocess
import re

from debug import de_bug
import PMSsystem




conf = config()

if not os.path.exists(conf.DIRECTORY):
    os.makedirs(conf.DIRECTORY)
    
os.chdir(conf.DIRECTORY)




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
        case "/PythonLSP":
            await PythonLSP(websocket, path)
        case "/debug":
            await _debug_socket(websocket, path)
        case "/stop":
            # receive the string "SIGINT" to stop the currently running process
            message = await websocket.recv()
            print("Received message:", message)
            if message:
                await PMSsystem.stop_current_process()
        case _: await websocket.send("Invalid path")



    
ws_server = websockets.serve(handler, conf.WS_HOST, conf.WS_PORT)
print("CodeRunner Server version 2.0")
print("TEST SERVER: Things may break")
print("Server started at port", conf.WS_PORT)
print("Relay started at address https://localhost:5000/")
print("Press Ctrl+C to stop the server")
asyncio.get_event_loop().run_until_complete(ws_server)
asyncio.get_event_loop().run_forever()