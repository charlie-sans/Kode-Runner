import PySide6
import PySide6.QtCore
import PySide6.QtGui
import PySide6.QtWidgets
import PySide6.QtWebEngineWidgets
import PySide6.QtWebEngineCore
import PySide6.QtWebSockets
import os
import sys
import json
import logging
import asyncio
import websockets
import configparser
import argparse
import time 
import threading
import requests
import coderunner_tools.discriptor.jsonthing as jsonthing
from coderunner_tools.discriptor.jsonthing import JsonCreatorWindow
#import textural
import http.server

#############
# C 2024 OpenStudio
# Websocket testing tool 
# all rights reserved
# This file is part of the OpenStudio software library for development and testing.
# THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND.
# ALL WARRANTIES, INCLUDING THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE, ARE EXPRESSLY DISCLAIMED.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY.
#############


class WebTester(PySide6.QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.jsonconfig = JsonCreatorWindow()
        self.setWindowTitle("Websocket Tester")
        self.layout = PySide6.QtWidgets.QHBoxLayout()  # Use QHBoxLayout instead of QVBoxLayout
        self.setLayout(self.layout)

        self.left_layout = PySide6.QtWidgets.QVBoxLayout()  # Create a QVBoxLayout for the left side
        self.layout.addLayout(self.left_layout)

        self.uri_label = PySide6.QtWidgets.QLabel("URI:")
        self.left_layout.addWidget(self.uri_label)

        self.uri_input = PySide6.QtWidgets.QLineEdit()
        self.left_layout.addWidget(self.uri_input)

        self.connect_button = PySide6.QtWidgets.QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect)
        self.left_layout.addWidget(self.connect_button)

        self.disconnect_button = PySide6.QtWidgets.QPushButton("Disconnect")
        self.disconnect_button.clicked.connect(self.disconnect)
        self.left_layout.addWidget(self.disconnect_button)

        self.message_label = PySide6.QtWidgets.QLabel("Message:")
        self.left_layout.addWidget(self.message_label)

        self.message_input = PySide6.QtWidgets.QPlainTextEdit()
        self.left_layout.addWidget(self.message_input)

        self.send_button = PySide6.QtWidgets.QPushButton("Send")
        self.send_button.clicked.connect(self.send)
        self.left_layout.addWidget(self.send_button)

        self.right_layout = PySide6.QtWidgets.QVBoxLayout()  # Create a QVBoxLayout for the right side
        self.layout.addLayout(self.right_layout)

        self.response_label = PySide6.QtWidgets.QLabel("Response:")
        self.right_layout.addWidget(self.response_label)

        self.response_output = PySide6.QtWidgets.QPlainTextEdit()
        self.right_layout.addWidget(self.response_output)
        
        # button to create the json window from os.system
        self.create_json_button = PySide6.QtWidgets.QPushButton("Create JSON")
        self.create_json_button.clicked.connect(self.jsonconfig.show)
        self.right_layout.addWidget(self.create_json_button)
        
        
        
        #!sidebar
        self.sidebar = PySide6.QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.sidebar)

        self.dark_mode_button = PySide6.QtWidgets.QPushButton("Toggle Dark Mode")
        self.dark_mode_button.clicked.connect(self.toggle_dark_mode)
        self.sidebar.addWidget(self.dark_mode_button)
        self.create_test_button = PySide6.QtWidgets.QPushButton("Run Test")
        self.create_test_button.clicked.connect(self.run_test)
        self.sidebar.addWidget(self.create_test_button)
        self.test_list = PySide6.QtWidgets.QListWidget()
        self.sidebar.addWidget(self.test_list)
        self.test_list.addItem("Test PMS")
        self.test_list.addItem("Test CodeWriter")
        self.test_list.addItem("Test P-L-S")
        self.test_list.addItem("Test Parser")
        
        
        # test linking
        self.test_list.itemClicked.connect(self.run_test)
        
        
        #!sidebar
        self.response = None

        self.webview = None
        self.websocketlink = None
        self.websocket = None
        self.responses = None
        self.backgroundColor = None
        self.textColor = None
        self.textSize = None
        self.Font = None
        self.foregroundcolor = None
        self.windowcolor = None
        self.sidecolor = None
        self.basecolor = None
        self.alternatebasecolor = None
        self.testslist = {}

        def jsonconfig_show():
            self.jsonconfig.show()
        def read_config():
            try:
                
                config = configparser.ConfigParser()
                config.read("config.ini")
                self.websocketlink = config["WEBSOCKET"]["link"]
                self.websocket = self.websocket()
                self.basecolor = config["COLORS"]["basecolor"]
                self.alternatebasecolor = config["COLORS"]["alternatebasecolor"]
                self.foregroundcolor = config["COLORS"]["foregroundcolor"]
                self.windowcolor = config["COLORS"]["windowcolor"]
                self.sidecolor = config["COLORS"]["sidecolor"]
                self.Font = config["FONTS"]["font"]
                self.textSize = config["FONTS"]["textsize"]
                self.textColor = config["FONTS"]["textcolor"]
                self.backgroundColor = config["FONTS"]["backgroundcolor"]
                # stylesheet defined in the config file
                stylesheet = None
                with open(config["STYLESHEET"]["stylesheet"], "r") as file:
                    stylesheet = file.read()
                self.setStyleSheet(stylesheet)
            except Exception as e:
                print(f"Error reading config file: {e}")
        
        read_config()
        
    
    def generate_test_list(self):
        files = os.listdir("tests")
        filelist = [f"tests/{file}" for file in files if file.endswith(".json")]
        for file in filelist:
            # file is a json file with the test data so we need to parse it
            with open(file, "r") as f:
                data = json.load(f)
                self.test_list.addItem(data["name"])
                filename = file.split(".")[0]
                self.testslist[filename] = data
                
    def run_test(self):
        test = self.test_list.currentItem().text()
        # use the file that we parsed earlier to get the test data
        test_data = self.testslist[test]
        if test_data["type"] == "Websocket":
            self.websocket.sendTextMessage(test_data["test_data"])
            data = self.websocket.receive()
            
            if data is None:
                self.response_output.appendPlainText("No response received")
                return
            
            # i love writing this BULLSHIT IN VR WTF BROOO
            if data != test_data["expected_response"]:
                self.response_output.appendPlainText(f"Test failed. Expected {test_data['expected_response']} but received {data}") # Print the response
                
        elif test_data["type"] == "http-get":
            response = requests.get(test_data["url"])
            self.response_output.appendPlainText(response.text)
            
        elif test_data["type"] == "http-post":
            response = requests.post(test_data["url"], data=test_data["test_data"])
            self.response_output.appendPlainText(response.text)
            
    def webview(self):
        self.webview = PySide6.QtWebEngineWidgets.QWebEngineView()
        self.layout.addWidget(self.webview)
        self.webview.load(PySide6.QtCore.QUrl("https://www.google.com"))
        
    def websocket(self):
        self.websocket = PySide6.QtWebSockets.QWebSocket()
        self.websocket.connected.connect(self.on_connected)
        self.websocket.disconnected.connect(self.on_disconnected)
        self.websocket.textMessageReceived.connect(self.on_message_received)
        self.websocket.open(PySide6.QtCore.QUrl(self.websocketlink))
        return self.websocket
   
    
    #!tests
    
    def test_pms(self):
        #TODO: Implement test_pms
        #self.websocket.sendTextMessage(message)
        pass
    
    def test_codewriter(self):
        pass #TODO: Implement test_codewriter
    
    def test_pylinterinpl(self):
        self.send() # Send the message
        if self.responses is None:
            self.response_output.appendPlainText("No response received")
            return
        diagnostics = json.loads(self.responses)
        self.response_output.clear()
        self.response_output.appendPlainText("Received diagnostics:")
        
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
        self.response_output.appendPlainText(diagnostics_string)
    #TODO: Implement test_pylinterinpl
    
    def test_parser(self):
        pass
    #TODO: Implement test_parser
    
    
    
    #!tests
    
    def connect(self):
        uri = self.uri_input.text()
        self.websocket = PySide6.QtWebSockets.QWebSocket()
        self.websocket.connected.connect(self.on_connected)
        self.websocket.disconnected.connect(self.on_disconnected)
        self.websocket.textMessageReceived.connect(self.on_message_received)
        self.websocket.open(PySide6.QtCore.QUrl(uri))

    def disconnect(self):
        self.websocket.close()

    def send(self):
        message = self.message_input.toPlainText()
        self.websocket.sendTextMessage(message)

    def on_connected(self):
        self.response_output.appendPlainText("Connected")

    def on_disconnected(self):
        self.response_output.appendPlainText("Disconnected")

    def on_message_received(self, message):
        self.response = message 
        self.response_output.appendPlainText(message)

    def run_test(self, item):
        test = self.test_list.currentItem().text()
        if test == "Test PMS":
            self.test_pms()
        elif test == "Test CodeWriter":
            self.test_codewriter()
        elif test == "Test linterimpl":
            self.test_pylinterinpl()
        elif test == "Test Parser":
            self.test_parser()
            
    def toggle_dark_mode(self):
        palette = self.palette()
        if palette.color(PySide6.QtGui.QPalette.Window).lightness() > 128:
            # Light mode, switch to dark mode
            palette.setColor(PySide6.QtGui.QPalette.Window, PySide6.QtGui.QColor(30, 30, 30))
            palette.setColor(PySide6.QtGui.QPalette.WindowText, PySide6.QtGui.QColor(200, 200, 200))
            palette.setColor(PySide6.QtGui.QPalette.Base, PySide6.QtGui.QColor(40, 40, 40))
            palette.setColor(PySide6.QtGui.QPalette.AlternateBase, PySide6.QtGui.QColor(50, 50, 50))
        else:
            # Dark mode, switch to light mode
            palette.setColor(PySide6.QtGui.QPalette.Window, PySide6.QtGui.QColor(240, 240, 240))
            palette.setColor(PySide6.QtGui.QPalette.WindowText, PySide6.QtGui.QColor(30, 30, 30))
            palette.setColor(PySide6.QtGui.QPalette.Base, PySide6.QtGui.QColor(255, 255, 255))
            palette.setColor(PySide6.QtGui.QPalette.AlternateBase, PySide6.QtGui.QColor(240, 240, 240))
        self.setPalette(palette)
app = PySide6.QtWidgets.QApplication([])
window = WebTester()
window.show()
window.generate_test_list()
app.exec()
