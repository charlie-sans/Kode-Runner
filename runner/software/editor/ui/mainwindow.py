from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox, QLabel, QListWidget, QListWidgetItem, QHBoxLayout, QTreeView, QSplitter, QFileSystemModel, QDockWidget
from PySide6.QtGui import QAction, QIcon, QKeySequence,QShortcut
from PySide6.QtCore import Qt, QSize, QDir, QFileInfo
from widgets.text_editor import TextEditor
from utils.service import Service
import os 
from widgets.console import Console
import sqlite3
class MainWindow(QMainWindow):
    def __init__(self, content):
        super().__init__()
        self.setWindowTitle("Text Editor")
        self.setGeometry(100, 100, 1000, 600)
        
        # Create a splitter for the file tree and editor
        self.splitter = QSplitter(Qt.Horizontal)

        
        # Create and set up the file tree
        self.file_tree = QTreeView()
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.currentPath())
        self.file_tree.setModel(self.file_model)
        self.file_tree.setRootIndex(self.file_model.index(QDir.currentPath()))
        self.file_tree.setColumnWidth(0, 250)
        self.file_tree.setAnimated(False)
        self.file_tree.setIndentation(20)
        self.file_tree.setSortingEnabled(True)
        self.file_tree.setWindowTitle("File System Viewer")
        self.file_tree.setMinimumWidth(250)
        
        # Connect double-click event to open file
        self.file_tree.doubleClicked.connect(self.open_file_from_tree)
        
        # Create the editor
        self.editor = TextEditor()
        self.console = Console()
        self.current_file = None  # Attribute to store the current file path
        
        # Create a dock widget for the console
        self.console_dock = QDockWidget("Console", self)
        self.console_dock.setWidget(self.console.window())
        self.console_dock.setAllowedAreas(Qt.BottomDockWidgetArea)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.console_dock)
        self.console_dock.hide()  # Initially hide the console

        # Add widgets to splitter
        self.splitter.addWidget(self.file_tree)
        self.splitter.addWidget(self.editor)
        
        # Set the splitter as the central widget
        self.setCentralWidget(self.splitter)
        
        if content:
            self.editor.setPlainText(content)
        
        self.create_menu()
        self.create_shortcuts()

    def connect_to_server(self):
        self.server = Service(5000)
        self.PMS_Client, self.Code_Client = self.server.start()

    def open_file_from_tree(self, index):
        path = self.file_model.filePath(index)
        if QFileInfo(path).isFile():
            try:
                with open(path, 'r') as f:
                    content = f.read()
                self.editor.setPlainText(content)
                self.current_file = path  # Cache the file path
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def create_shortcuts(self):
        # Shortcut for saving (Ctrl+S)
        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self.save_file)

        # Shortcut for toggling console (Ctrl+`)
        console_shortcut = QShortcut(QKeySequence("Ctrl+k"), self)
        console_shortcut.activated.connect(self.toggle_console)

    def toggle_console(self):
        if self.console_dock.isVisible():
            self.console_dock.hide()
        else:
            self.console_dock.show()

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        
        open_action = file_menu.addAction('Open')
        open_action.triggered.connect(self.open_file)
        
        save_action = file_menu.addAction('Save')
        save_action.triggered.connect(self.save_file)
        
        exit_action = file_menu.addAction('Exit')
        exit_action.triggered.connect(self.close)
        
        send_file_action = file_menu.addAction('Send File to Server')
        send_file_action.triggered.connect(self.send_file_to_server)
        
        send_config_action = file_menu.addAction('Send Config to Server')
        send_config_action.triggered.connect(self.send_config_to_server)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
        
        connect_to_server_action = file_menu.addAction('Connect to Server')
        connect_to_server_action.triggered.connect(self.connect_to_server)

        console_window = menubar.addMenu('Console')
        console_action = console_window.addAction('Toggle Console')
        console_action.triggered.connect(self.toggle_console)
        console_action.setShortcut(QKeySequence("Ctrl+`"))

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Python Files (*.py);;All Files (*)")
        if filename:
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                self.editor.setPlainText(content)
                self.current_file = filename  # Cache the file path
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
                
    def save_file(self):
        if self.current_file:
            try:
                content = self.editor.toPlainText()
                with open(self.current_file, 'w') as f:
                    f.write(content)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            self.save_file_as()

    def save_file_as(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File As", "", "Python Files (*.py);;All Files (*)")
        if filename:
            try:
                content = self.editor.toPlainText()
                with open(filename, 'w') as f:
                    f.write(content)
                self.current_file = filename  # Cache the new file path
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def send_file_to_server(self):
        if self.current_file:
            with open(self.current_file, 'r') as f:
                content = f.read()
            self.PMS_Client.send(content)
            
    def send_config_to_server(self):
        # find the config file in the current directory 
        config_file = os.path.join(os.path.dirname(self.current_file), "config.json")
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                content = f.read()
            self.PMS_Client.send(content)
            while True:
                response = self.PMS_Client.recv()
                # the contents of the response is the output from the terminal that was piped to the client
                self.console.append(response)
                # terminal could be a clear command which would require clearing the console
                if response == "[H":
                    self.console.clear()
                # if the response is a prompt from the terminal then we can assume that the config has been sent and we can break the loop
                elif response == ">>>":
                    break

    def send_code_to_server(self):
        if self.current_file:
            with open(self.current_file, 'r') as f:
                content = f.read()
            self.Code_Client.send(content)


