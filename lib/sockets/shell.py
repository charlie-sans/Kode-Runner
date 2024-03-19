"""
(C) 2024 sinkhole.wattlefoxxo.com 
all rights reserved
"""

import asyncio
import websockets
import subprocess
import pty
import os
import pyte
import signal

TTY_WIDTH = 170
TTY_HEIGHT = 28

colour_map = {
    "black": "000000",
    "red": "ff0000",
    "green": "00ff00",
    "brown": "ffff00",
    "blue": "0000ff",
    "magenta": "ff00ff",
    "cyan": "00ffff",
    "white": "ffffff",
    "default": "ffffff"
}

key_map = {
    "ctrl+A": b'\x01',
    "ctrl+B": b'\x02',
    "ctrl+C": b'\x03',
    "ctrl+D": b'\x04',
    "ctrl+E": b'\x05',
    "ctrl+F": b'\x06',
    "ctrl+G": b'\x07',
    "ctrl+H": b'\x08',
    "ctrl+I": b'\x09',
    "ctrl+J": b'\x0A',
    "ctrl+K": b'\x0B',
    "ctrl+L": b'\x0C',
    "ctrl+M": b'\x0D',
    "ctrl+N": b'\x0E',
    "ctrl+O": b'\x0F',
    "ctrl+P": b'\x10',
    "ctrl+Q": b'\x11',
    "ctrl+R": b'\x12',
    "ctrl+S": b'\x13',
    "ctrl+T": b'\x14',
    "ctrl+U": b'\x15',
    "ctrl+V": b'\x16',
    "ctrl+W": b'\x17',
    "ctrl+X": b'\x18',
    "ctrl+Y": b'\x19',
    "ctrl+Z": b'\x1A',
    "ctrl+[": b'\x1B',
    "ctrl+\\": b'\x1C',
    "ctrl+]": b'\x1D',
    "ctrl+^": b'\x1E',
    "ctrl+_": b'\x1F'
}

async def process_screen(buffer):
    output = []
    for row in range(TTY_HEIGHT):
        line = ""
        for col in range(TTY_WIDTH):
            cell = buffer[row][col]

            colour = cell.fg
            if cell == " ":
                continue
            if (colour in colour_map):
                colour = colour_map[cell.fg]

            line += f"<color=#{colour}>{cell.data}</color>"
        output.append(line)
    return output


async def shell(websocket, path):
    screen = pyte.Screen(TTY_WIDTH, TTY_HEIGHT)
    stream = pyte.Stream(screen)

    master_fd, slave_fd = pty.openpty()

    process = await asyncio.create_subprocess_exec(
        "/bin/bash",
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        start_new_session=True,
        env={"TERM": "xterm"}
    )

    async def send_shell():
        while True:
            output = await asyncio.get_event_loop().run_in_executor(None, os.read, master_fd, 1024)
            if output:
                stream.feed(output.decode())
                display_content = "\n".join(await process_screen(screen.buffer))
                await websocket.send(display_content)
    
    async def receive_shell():
        async for command in websocket:
            if command in key_map:
                os.write(master_fd, key_map[command])
            else:
                os.write(master_fd, command.encode())

    await asyncio.gather(
        send_shell(),
        receive_shell()
    )

