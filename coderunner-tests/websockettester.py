import websockets
import asyncio
import os 
import json
import sys
import logging

logging.basicConfig(level=logging.INFO)

async def test_pylinterinpl():
    uri = 'ws://localhost:8765'
    async with websockets.connect(uri) as websocket:
        await websocket.send('prnt("Hello, World!')
        response = await websocket.recv()
        diagnostics = json.loads(response)

# Pretty print the diagnostics
        for diag in diagnostics:
            print(f"File: {diag['file']}")
            print(f"Severity: {diag['severity']}")
            print(f"Message: {diag['message']}")
            print(f"Line: {diag['range']['start']['line']} to {diag['range']['end']['line']}")
            print(f"Character: {diag['range']['start']['character']} to {diag['range']['end']['character']}")
            print(f"Rule: {diag.get('rule', 'N/A')}")
            print("-" * 40)  # Separator for readability
    
asyncio.get_event_loop().run_until_complete(test_pylinterinpl())
asyncio.get_event_loop().run_forever()