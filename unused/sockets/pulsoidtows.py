import json as jsons
import asyncio
import websockets
import os
import requests
# pulsoid heartrate to websocket server

token = ""

# heartrate data socket
# wss://dev.pulsoid.net/api/v1/data/real_time

async def  heartbeat(websocket):
    async with websockets.connect(f'wss://dev.pulsoid.net/api/v1/data/real_time?access_token={token}') as ws:
        while True:
            try:
                data = await ws.recv()
                json = jsons.loads(data)
                await websocket.send(json['data']['heart_rate'])
            except websockets.exceptions.ConnectionClosedOK:
                break

async def pulsoidtows(websocket, path):
    try:
        await heartbeat(websocket)
    except websockets.exceptions.ConnectionClosedOK:
        pass
    
start_server = websockets.serve(pulsoidtows, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
