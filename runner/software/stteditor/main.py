import websockets
import asyncio
import json
import os
import sys
import time
import logging
import traceback
import pyaudio
import pygame
from markdown_preprocessor import MarkdownPreprocessor
import markdown
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

# Configure logging
logging.basicConfig(level=logging.INFO)

# speech to text based markdown editor

# text comes in through websocket
# text is converted to markdown
# markdown is written to the system or to the clipboard

socket_url = "ws://localhost:8766"
rec_url = "ws://localhost:6789"
websocket_rec = None
websocket_send = None
main_loop = None
message_queue = asyncio.Queue()
mark = MarkdownPreprocessor()



async def play_audio(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    # set the volume
    pygame.mixer.music.set_volume(0.5)
    # play the audio file
    pygame.mixer.music.play()

async def get_text(websocket): # this saves us the trouble of having to get around [speechEnded] in the main loop   
    text = await websocket.recv()
    if text == "[speechEnded]":
        text = await websocket.recv()
        return text



async def run():
    global websocket_rec, websocket_send
    try:
        websocket_rec = await websockets.connect(rec_url)
        websocket_send = await websockets.connect(socket_url)
    except ConnectionRefusedError as e:
        logging.error(f"Connection refused: {e}")
        return
    except websockets.exceptions.InvalidStatusCode as e:
        logging.error(f"Invalid status code: {e.status_code}")
        logging.error(f"Headers: {e.headers}")
        return
    except Exception as e:
        logging.error(f"Error connecting to WebSocket: {e}")
        logging.error(traceback.format_exc())
        return
    await run_editor(websocket=websocket_rec, path="")
    asyncio.get_event_loop().run_forever()

async def run_editor(websocket, path):
    commands = ["bold", "italic", "header", "link", "image", "list", "code", "create file", "exit", "create list", "create link", "create image", "create code"]
    completer = WordCompleter(commands, ignore_case=True)
    session = PromptSession(completer=completer)

    print("Welcome to the Markdown Editor! Type 'exit' to quit.")
    while True:
        try:
            message = await websocket.recv()
            print(f"markdown list contains {await mark.get_item_count()} items")
            
            match message:
                case "remove last item" | "delete last item":
                    message = await mark.remove_last_item()
                    print(f"Removed last item: {message}")
                    await websocket_send.send(f"Removed last item: {message}")
                case "italic" | "emphasis":
                    await mark.italic_text(websocket, websocket_send)
                case "code" | "code block":
                    await mark.create_code_block(websocket, websocket_send)
                case "image" | "picture":
                    await mark.create_image(websocket, websocket_send)
                case "star list" | "unordered list":
                    await mark.create_list_stars(websocket, websocket_send)
                        
                case "clear list" | "clear markdown":
                    await mark.clear_queue()
                    await websocket_send.send("list cleared")
                case "create file" | "new file":
                    await mark.create_file(websocket_rec, websocket_send)
                    
                case "create list" | "new list":
                    await mark.create_list(websocket_rec, websocket_send)
                    
                case "bold" | "strong":
                    await mark.bold_text(websocket, websocket_send)
                        
                case "header" | "heading":
                   await mark.create_header(websocket, websocket_send)
                        
                case "link" | "hyperlink":
                    await mark.create_link(websocket, websocket_send)
                        
                case "section" | "subsection":
                    await mark.create_section(websocket, websocket_send)
                        
                case "end section" | "end subsection":
                    await mark.end_section(websocket, websocket_send)
                        
                case "new line" | "line break":
                    await message_queue.put("\n")
                    await websocket_send.send("\n")
                    
                case "new paragraph"  | "paragraph break":
                    await message_queue.put("\n\n")
                    await websocket_send.send("\n\n")
                    
                case "dump markdown" | "save markdown":
                    await play_audio("speak_prompt.ogg")
                    text = await get_text(websocket) # name of file
                    print(f"Dumping markdown to {text}")
                    # write the queue to a file
                    with open(text + ".md", "w") as f:
                        f.write(await mark.get_all_items())
                    print("Dumped markdown to file")
                    await websocket_send.send("markdown dumped")
                    
                case "print markdown" | "print":
                    print("Printing markdown")  
                    await websocket_send.send(await mark.get_all_items())
                    await websocket_send.send("markdown printed")
                    
                case "exit" | "quit":
                    print("Exiting")
                    break
                
                case "load markdown" | "load":
                    await play_audio("speak_prompt.ogg")
                    text = await get_text(websocket)
                    print(f"Loading markdown from {text}")
                    with open(text, "r") as f:
                        for line in f:
                            await message_queue.put(line)
                    print("Loaded markdown")
                    await websocket_send.send("markdown loaded")
                    
                case _:
                    if message != "[speechEnded]":
                        await message_queue.put(message + "\n")
                        await websocket_send.send(message + "\n")
                        
        except Exception as e:
            logging.error(f"Error in run_editor: {e}")
            logging.error(traceback.format_exc())
            break

async def start_editor(websocket, path):
    logging.info("Starting editor")
    await run_editor(websocket, path)

def main():
    print("Server started")
    asyncio.run(run())

if __name__ == "__main__":
    main()