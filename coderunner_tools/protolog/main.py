import tkinter as tk
from tkinter import filedialog, Toplevel, Text
import asyncio
import websockets
import json

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Text Editor")
        
        self.text_area = tk.Text(self.root)
        self.text_area.pack(expand=1, fill='both')
        
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        
        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Send to Server", command=self.send_to_server)
        file_menu.add_command(label="Receive from Server", command=self.receive_from_server)
        
        config_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Config", menu=config_menu)
        config_menu.add_command(label="Send Config", command=self.send_config)
        
        self.code_server_uri = "ws://localhost:8765/code"  # Change this to your code server URI
        self.config_server_uri = "ws://localhost:8765/PMS"  # Change this to your config server URI

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_area.get(1.0, tk.END))

    async def send_to_server_async(self):
        async with websockets.connect(self.code_server_uri) as websocket:
            text = self.text_area.get(1.0, tk.END)
            await websocket.send(text)
            response = await websocket.recv()
            print(f"Server response: {response}")

    def send_to_server(self):
        asyncio.run(self.send_to_server_async())

    async def receive_from_server_async(self):
        async with websockets.connect(self.code_server_uri) as websocket:
            await websocket.send("REQUEST_TEXT")
            text = await websocket.recv()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, text)

    def receive_from_server(self):
        asyncio.run(self.receive_from_server_async())

    async def send_config_async(self):
        async with websockets.connect(self.config_server_uri) as websocket:
            config = {
                "font_size": 12,
                "theme": "light"
            }
            await websocket.send(json.dumps(config))
            response = await websocket.recv()
            self.show_response(response)

    def send_config(self):
        asyncio.run(self.send_config_async())

    def show_response(self, response):
        response_window = Toplevel(self.root)
        response_window.title("Server Response")
        response_text = Text(response_window)
        response_text.pack(expand=1, fill='both')
        response_text.insert(tk.END, response)

if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()