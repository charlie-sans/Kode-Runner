import asyncio
import websockets
import pty
import os
import subprocess
async def handle_ws(websocket, path):
    while True:
        code = await websocket.recv()
        command = "python3 recivx0x23.py"
        with open("recivx0x23.py", "w") as file:
            file.write(code)
        
        # read from the pty live

        
        result = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while result.poll() is None:
            output = result.stdout.readline()
            await websocket.send(output)
        
        
        

       
        
        
ws_server = websockets.serve(handle_ws, "127.0.0.1", 5000)

asyncio.get_event_loop().run_until_complete(ws_server)
asyncio.get_event_loop().run_forever()