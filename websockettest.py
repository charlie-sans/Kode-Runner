
import websockets
import asyncio

async def handler(websocket, path):
    print(websocket, path)
    match path:
        case "/echo":
            await echo(websocket, path)
        case "/hello":
            await hello(websocket, path)
    
async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)
        
async def hello(websocket, path):
    await websocket.send("Hello World!")




if __name__ == "__main__":
    start_server = websockets.serve(handler, "localhost", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
    