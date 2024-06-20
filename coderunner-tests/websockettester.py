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
        diagnostics_string = ""
        for diag in diagnostics:
            diagnostics_string += f"File: {diag['file']}\n"
            diagnostics_string += f"Severity: {diag['severity']}\n"
            diagnostics_string += f"Message: {diag['message']}\n"
            diagnostics_string += f"Line: {diag['range']['start']['line']} to {diag['range']['end']['line']}\n"
            diagnostics_string += f"Character: {diag['range']['start']['character']} to {diag['range']['end']['character']}\n"
            diagnostics_string += f"Rule: {diag.get('rule', 'N/A')}\n"
            diagnostics_string += "-" * 40 + "\n"  # Separator for readability
    
asyncio.get_event_loop().run_until_complete(test_pylinterinpl())
asyncio.get_event_loop().run_forever()