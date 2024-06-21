import threading 
import json
import asyncio
import PySide6.QtWidgets as QtWidgets
import websockets

class JsonCreatorWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("json creator")
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.key = None
        self.value = None
        self.json = {}
        self.create_button = None
        self.add_button = None
        self.handler = None
        self.key_value_pairs = {}
        self.client = None

        self.textfield = QtWidgets.QLineEdit()
        self.layout.addWidget(self.textfield)
        
        self.jsontemplates = QtWidgets.QComboBox()
        self.jsontemplates.addItems([ "key value", "oobject key"])
        self.layout.addWidget(self.jsontemplates)
        
        
        self.create_button = QtWidgets.QPushButton("Create JSON")
        self.layout.addWidget(self.create_button)
        self.create_button.clicked.connect(self.create_json)
        
        
        self.show()
        
    def create_json(self):
       # take each key-value pair widget and add it to the json object
       for key, value in self.key_value_pairs.items():
           self.json[key] = value
           self.json = json.dumps(self.json)
           self.client.send(self.json)
        

        
    def closeEvent(self, event):
        if self.json:
            with open("json.json", "w") as f:
                f.write(self.json)
        event.accept()
    def jsontemplates(self):
        # get the selected json template
        template = self.jsontemplates.currentText()
        match template:
            case "key value":
                #append a key value pair template to the text box layout
                pass
            case "object key":
                self.handler = self.object_key
    
    def key_value(self):
        return self.textfield.text()
    

    
    def start_server(self):
        with websockets.connect("ws://localhost:8765") as websocket:
            self.client = websocket
            self.client.send("json connected")
            while True:
                data = self.client.recv()
                self.handler(data)
        
    def stop_server(self): # stop the server
        self.server.shutdown()
        self.server.server_close()
        self.server = None
        self.client = None
        self.key = None
        self.value = None
        self.json = None
        
    
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = JsonCreatorWindow()
    window.show()
    # server_thread = threading.Thread(target=window.start_server)
    # server_thread.start()
    
    
    app.exec()
    