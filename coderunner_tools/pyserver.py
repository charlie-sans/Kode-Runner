import asyncio
import json
import subprocess
import tempfile
import os
import websockets

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

async def handler(websocket, path):
    async for message in websocket:
        code = message
        diagnostics = await analyze_code(code)
        await websocket.send(diagnostics)

start_server = websockets.serve(handler, "localhost", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
