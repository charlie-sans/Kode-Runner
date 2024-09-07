import asyncio
import websockets
import subprocess
import pty
import os

async def shell(websocket, path):
    master_fd, slave_fd = pty.openpty()

    process = await asyncio.create_subprocess_exec(
        '/bin/bash',
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        start_new_session=True,
        env={'TERM': 'xterm'}
    )

    async def send_shell():
        while True:
            output = await asyncio.get_event_loop().run_in_executor(None, os.read, master_fd, 1024)
            if output:
                await websocket.send(output.decode())
    
    async def receive_shell():
        async for command in websocket:
            os.write(master_fd, command.encode())

    await asyncio.gather(
        send_shell(),
        receive_shell()
    )

start_server = websockets.serve(shell, "localhost", 500)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()