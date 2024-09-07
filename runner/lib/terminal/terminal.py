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

async def terminal(websocket, path):
    try:
        
    except websockets.exceptions.ConnectionClosedError:
        pass
    except Exception as e:
        await websocket.send("An error occured while trying to run the terminal")
        logging.error(traceback.format_exc())