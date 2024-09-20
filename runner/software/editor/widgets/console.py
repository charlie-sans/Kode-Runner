import sys
import json
import logging
import os
import traceback
import time
import websockets
from PySide6.QtWidgets import QTextEdit
import re

class Console:
    def __init__(self):
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.logger = logging.getLogger(__name__)

    def window(self):
        return self.console

    def log_message(self, message):
        self.console.append(message)

    def clear_console(self):
        self.console.clear()

    def highlight_text(self, text):
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        text = ansi_escape.sub(self.ansi_to_html, text)
        return text

    def ansi_to_html(self, match):
        ansi_code = match.group()
        ansi_to_html_map = {
            '\033[91m': '<span style="color:red;">',
            '\033[92m': '<span style="color:green;">',
            '\033[93m': '<span style="color:yellow;">',
            '\033[94m': '<span style="color:blue;">',
            '\033[0m': '</span>',
            # Add more mappings as needed
        }
        return ansi_to_html_map.get(ansi_code, '')

    def log_message_with_highlight(self, message):
        highlighted_message = self.highlight_text(message)
        self.console.append(highlighted_message)
        self.logger.info(f"Message logged with highlight: {message}")