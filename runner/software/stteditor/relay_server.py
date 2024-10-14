import asyncio
import websockets
import logging
import traceback

logging.basicConfig(level=logging.DEBUG)

message_queue = asyncio.Queue()
connected_clients = set()

async def relay_handler(websocket, path):
    global connected_clients
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            logging.info(f"Received message: {message}")
            await message_queue.put(message)
            # Broadcast the message to all connected clients
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
    except Exception as e:
        logging.error(f"Error in relay_handler: {e}")
        logging.error(traceback.format_exc())
    finally:
        connected_clients.remove(websocket)

async def relay_server():
    server = await websockets.serve(relay_handler, "localhost", 8766)
    logging.info("Relay server started on ws://localhost:8766")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(relay_server())