import websockets
import asyncio
import json
import os
import sys
import time
import threading
import traceback
import logging
import subprocess
import signal
import psutil
import re
import platform
import shutil


"""
terminal for CodeRunner.

this module is responsible for taking in json commands from the client and doing actions based on the command.

commands:
    - list files in a a project directory
    - run a command in a project directory
    - get the current working directory
    - zip a project directory 
    - unzip a project directory
    - get the current platform
    
"""

project_dir = "software/code/"


async def run_command(websocket, command, cwd):
    if cwd:
        os.chdir(cwd)
        
  print("Executing command: " + command)
    print("Command: " + command)
    child = pexpect.spawn(command, encoding="utf-8")
    while True:
        try:
            index = child.expect(['\n', '.', pexpect.EOF, pexpect.TIMEOUT], timeout=1)
            if index == 0 or index == 1:
                decolorised_text = re.sub(r'\x1b\[[0-9;]*m', '', child.after)
                await websocket.send(decolorised_text)
            elif index == 2:
                break
        except pexpect.exceptions.TIMEOUT:
            break
async def terminal(websocket, path):
    try:
        while True:
            data = await websocket.recv()
            data = json.loads(data)
            if data["type"] == "command":
                command = data["command"]
                match command:
                    case "list_files":
                        project = data["project"]
                        files = os.listdir(project_dir + project)
                        await websocket.send(json.dumps(files))
                    case "run_command":
                        project = data["project"]
                        command = data["command"]
                        cwd = project_dir + project
                        await run_command(websocket, command, cwd)
                    case "get_cwd":
                        await websocket.send(os.getcwd())
                    case "zip_project":
                        project = data["project"]
                        shutil.make_archive(project_dir + project, 'zip', project_dir, project)
                        await websocket.send("done")
                        await websocket.send(project + ".zip" + " has been created at " + project_dir)
                    case "unzip_project":
                        project = data["project"]
                        shutil.unpack_archive(project_dir + project, project_dir)
                        await websocket.send("done")
                        await websocket.send(project + " has been unzipped at " + project_dir)
                    case "get_platform":
                        await websocket.send(platform.system())

        
                    case _:
                        await websocket.send("command not found")
    except websockets.exceptions.ConnectionClosedError:
        print("Connection closed")
        return