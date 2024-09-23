
import os
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
import sqlite3
from ui.welcomewindow import WelcomeWindow

def main():
    app = QApplication(sys.argv) # start the welcome window
    if os.path.exists("projects.db"):
        pass
    else:
         # make the dB

         conn = sqlite3.connect("projects.db")
         cursor = conn.cursor()
         cursor.execute("CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, path TEXT)")
         conn.commit()
         conn.close()
    window = WelcomeWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    
