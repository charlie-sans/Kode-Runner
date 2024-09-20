import sys
from PySide6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QTextCursor, QTextCharFormat, QColor
from utils.syntax_highlighter import SyntaxHighlighter

class TextEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.highlighter = SyntaxHighlighter(self.document())
        self.setTabStopDistance(40)
        
        font = QFont("Monospace", 12)
        self.setFont(font)
        
        self.cursorPositionChanged.connect(self.highlight_current_line)
        
    def highlight_current_line(self):
        cursor = self.textCursor()
        selection = QTextEdit.ExtraSelection()
    
        selection.format.setBackground(QColor(255, 255, 255, 128))  # Alpha value 128 makes it 50% transparent
        
        selection.cursor = cursor
        selection.format.setProperty(QTextCharFormat.FullWidthSelection, True)
        self.setExtraSelections([selection])
    