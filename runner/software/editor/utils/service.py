import websockets 
import asyncio
import json
import logging
import os 
import sys
import traceback
import time

from utils.klog import logging



class Service:
    def __init__(self, port):
        
        self.port = port
        

    

    def start(self):
        self.PMS_Client = websockets.connect(f"ws://localhost:{self.port}/PMS")
        self.Code_Client =  websockets.connect(f"ws://localhost:{self.port}/Code")
        print("Connected to server")
        print(self.PMS_Client)
        print(self.Code_Client)
        return self.PMS_Client, self.Code_Client
        
    async def stop(self):
        await self.PMS_Client.close()
        await self.Code_Client.close()
   
        
    async def send(self, client, message):
        """sends message to client

        Args:
            client (self): client to send message to
            message (string): message to send
        """
        stopped = False
        await client.send(message)
        while not stopped:
            try:
                response = await self.receive(client)
                if response is not None:
                    stopped = True
                    return response
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                stopped = False

    
    async def receive(self, client):
        """recieve message from client

        Args:
            client (self): client to recieve message from

        Returns:
            strong: message from client
        """
        data = None
        try:
            while data is None:
                data = await client.recv()
       
                return data
        except websockets.exceptions.ConnectionClosedError:
            print("Connection closed")
            return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None


