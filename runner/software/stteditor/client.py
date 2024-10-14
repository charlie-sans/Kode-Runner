import asyncio
import websockets
import logging
import traceback

logging.basicConfig(level=logging.DEBUG)

async def client():
    try:
        async with websockets.connect("ws://localhost:8766") as websocket:
            while True:
                message = await websocket.recv()
                print(f"Received message: {message}")
    except Exception as e:
        logging.error(f"Error in client: {e}")
        logging.error(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(client())