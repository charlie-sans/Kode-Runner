import websockets 
import asyncio
import os
import pexpect


async def term():
    term = pexpect.spawn("python3 lib/server.py")
    # get the contents of the terminal and send it to the websocket
    return term
    

# start the server and connect to the relay server from the one we just started

async def relay():
    terminal = await term()
    print(terminal.before)
    async with websockets.connect("ws://localhost:5000/relay") as relay:
        while True:
            try:
                index = terminal.expect(['.', '\n', pexpect.EOF, pexpect.TIMEOUT], timeout=1)
                if index == 0 or index == 1:
                    await websocket.send(terminal.before)
                elif index == 2:
                    #await websocket.send(child.before)
                    break
            except pexpect.exceptions.TIMEOUT as e:
                print( f"Execution timed out {e}", "ERROR")
                break
            
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(relay())
    asyncio.get_event_loop().run_forever()