from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox, QLabel, QListWidget, QListWidgetItem, QHBoxLayout, QTreeView, QSplitter, QFileSystemModel, QDockWidget, QInputDialog
from PySide6.QtGui import QAction, QIcon, QKeySequence,QShortcut
from PySide6.QtCore import Qt, QSize, QDir, QFileInfo
import os
import sqlite3
from ui.mainwindow import MainWindow    
from widgets.text_editor import TextEditor



from widgets.console import Console
class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome")
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        text_header = QLabel("Welcome to the Text Editor!")
        layout.addWidget(text_header)
        open_editor_button = QPushButton("Open Editor")
        open_editor_button.clicked.connect(self.open_editor)
        layout.addWidget(open_editor_button)
        # set the size of the button
        open_editor_button.setFixedSize(QSize(200, 50))
        
        project_button = QPushButton("Create Project")
        project_button.clicked.connect(self.create_project)
        layout.addWidget(project_button)
        # set the size of the button
        project_button.setFixedSize(QSize(200, 50))

        project_list = QListWidget()
        project_list.setFixedSize(QSize(200, 50))   
        layout.addWidget(project_list)
        self.project_list = project_list
        self.add_project_to_list()
        self.project_name = None
        self.project_path = None


        if os.path.exists("projects.db"):
            self.add_project_to_list()
        else:
            # make the dB
            conn = sqlite3.connect("projects.db")
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, path TEXT)")
            conn.commit()
            conn.close()
        



        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
        
    def open_editor(self):
        self.main_window = MainWindow("")
        self.main_window.show()
        self.close()
        
    def open_editor_with_text(self, file_path):
        initial_text = None
        file = QFileDialog.getOpenFileName(self, "Open File", "", "Python Files (*.py);;All Files (*)")
        if file[0]:
            with open(file[0], 'r') as f:
                initial_text = f.read()
                
        self.main_window = MainWindow(initial_text)
        self.main_window.show()
        self.close()

    def create_project(self, project_path):
        project_name = QInputDialog.getText(self, "Create Project", "Enter project name:")
        if project_name[1]: 
            project_path = QFileDialog.getExistingDirectory(self, "Select Project Directory")
            if project_path:
                project_path = os.path.join(project_path, project_name[0])
                os.makedirs(project_path)
                self.project_path = project_path
                self.project_name = project_name[0]
                self.create_project_files()
                # open the project on the readme file
                self.open_editor_with_text(os.path.join(project_path, "README.md"))
                # create a new project in the database
                self.create_project_in_database()

    def create_project_in_database(self):
        conn = sqlite3.connect("projects.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, path TEXT)")
        cursor.execute("INSERT INTO projects (name, path) VALUES (?, ?)", (self.project_name, self.project_path))
        conn.commit()
        conn.close()

    def get_projects_from_database(self):
        if os.path.exists("projects.db"):
            conn = sqlite3.connect("projects.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects")
            projects = cursor.fetchall()

            conn.close()
            return projects
        else:
            # create the dB
            conn = sqlite3.connect("projects.db")
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, path TEXT)")
            conn.commit()
            conn.close()
            return []



    def add_project_to_list(self):
        projects = self.get_projects_from_database()
        for project in projects:
            project_name = project[1]  # Assuming project[1] contains the project name
            project_item = QListWidgetItem(project_name)  # Use a local variable instead of self.project_name
            project_item.setIcon(QIcon("resources/icons/project.png"))  # Set your icon here
            self.project_list.addItem(project_item)

    def create_project_files(self):

        project_files = ["main.py", "README.md", "LICENSE"]
        for file in project_files:
            with open(os.path.join(self.project_path, file), 'w') as f:
                f.write("")

    def add_project_to_list(self):  
        projects = self.get_projects_from_database()
        for project in projects:
            project_name = project[1]  # Assuming project[1] contains the project name
            project_item = QListWidgetItem(project_name)  # Use a local variable instead of self.project_name
            project_item.setIcon(QIcon("resources/icons/project.png"))  # Set your icon here
            self.project_list.addItem(project_item)

    def open_project(self):


        project_item = self.project_list.currentItem()
        if project_item:
            project_path = os.path.join(self.project_path, project_item.text())
            self.open_editor_with_text(project_path)

if __name__ == "__main__":
    app = QApplication([])
    welcome_window = WelcomeWindow()
    welcome_window.show()
    app.exec()
