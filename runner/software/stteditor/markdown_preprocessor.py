from email import message
import json
import re   # Regular expression
import asyncio
import websockets
import logging
import traceback
import markdown
import os
import sys
import time
import pyaudio
import pygame
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

class MarkdownPreprocessor:
    def __init__(self) -> None:
        self._markdown = ""
        self.message_queue = asyncio.Queue()
        
    async def play_audio(self,
                         filename):
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        # set the volume
        pygame.mixer.music.set_volume(0.5)
        # play the audio file
        pygame.mixer.music.play()

    async def get_text(self,websocket): # this saves us the trouble of having to get around [speechEnded] in the main loop
        text = await websocket.recv()
        if text == "[speechEnded]":
            text = await websocket.recv()
            return text
    
    async def get_markdown(self):
        return self.message_queue._queue # This is a list of messages
    
    async def create_list(self,websocket_rec,websocket_send):
        await self.play_audio("start_prompt.mp3")
        message = await websocket_rec.recv()
        if message == "[speechEnded]":
            await self.play_audio("speak_prompt.ogg")
            name = await websocket_rec.recv()
            print(f"{name}:")
            await self.message_queue.put(f"{name}:\n")
            await websocket_send.send(f"{name}:\n")
            while True :
                try:
                    message = await asyncio.wait_for(websocket_rec.recv(), timeout=5.0)
                    print(f"Received list item: '{message}'")  # Debug statement
                    if message.strip() == "end list":
                        print("Ending list")  # Debug statement
                        break
                    elif message == "[speechEnded]":
                        message = await websocket_rec.recv()
                        if message.strip() == "stop list":
                            print("Ending list")
                            break
                        print(f"  - {message}")
                        await self.message_queue.put(f"  - {message}\n")
                        await websocket_send.send(f"  - {message}\n")
                except asyncio.TimeoutError:
                    print("Timeout waiting for list item. Ending list.")  # Debug statement
                    break
    async def remove_last_item(self):
        self.message_queue._queue.pop(-1) # should remove the last item in the list from the bottom of the list
        
    async def peek_queue(self):
        return list(self.message_queue._queue)

    async def clear_queue(self):
        while not self.message_queue.empty():
            self.message_queue.get_nowait()

    async def get_latest_item(self):
        return self.message_queue._queue[-1]
    
    async def get_item_count(self):
        return len(self.message_queue._queue)

    async def get_first_item(self):
        return self.message_queue._queue[0]
    async def remove_first_item(self):
        self.message_queue._queue.pop(0)

    async def remove_last_item(self):
        self.message_queue._queue.pop()

    async def get_all_items(self):
        items = self.message_queue._queue
        # convert the list to a string
        return ''.join(items)  # This is the markdown
    async def remove_items(self,websocket_rec,websocket_send):
        # user should say a number of items to remove
        # we should remove that number of items from the queue
        
        # get the number of items to remove
        message = await self.get_text(websocket_rec)
        # remove the items
        for i in range(int(message)):
            self.message_queue._queue.pop()
    
    async def bold_text(self,websocket_rec,websocket_send):
        await self.play_audio("speak_prompt.ogg")
        message = await websocket_rec.recv()
        if message == "[speechEnded]":
            message = await websocket_rec.recv()
            print(f"**{message}**")
            await self.message_queue.put(f"**{message}**\n")
            await websocket_send.send(f"**{message}**\n")
    
    async def create_link(self,websocket_rec,websocket_send):
        await self.play_audio("speak_prompt.ogg")
        message = await self.get_text(websocket_rec)  
        print(f"[{message}]")
        await self.message_queue.put(f"[{message}]\n")
        await websocket_send.send(f"[{message}]\n")
            
    async def create_section(self,websocket_rec,websocket_send):
        await self.play_audio("speak_prompt.ogg")
        message = await self.get_text(websocket_rec)        
    
    async def create_header(self,websocket_rec,websocket_send):
            await self.play_audio("speak_prompt.ogg")
            message = await self.get_text(websocket_rec)  
            print(f"# {message}")
            await self.message_queue.put(f"# {message}\n")
            await websocket_send.send(f"# {message}\n")
            
                
    async def create_file(self,websocket_rec,websocket_send):
        await self.play_audio("start_prompt.mp3")
        message = await self.get_text(websocket_rec)
        print(f"Creating file: {message}")
        with open(message + ".md", "w") as f:
            f.write("")
        print("File created")
        await websocket_send.send("file created")