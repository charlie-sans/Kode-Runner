import json
import os
from PySide6.QtCore import QRegularExpression, Qt
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor

class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.highlightingRules = []
        self.colors = {}

        self.load_keywords()

    def load_keywords(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, '..', 'resources', 'colors.json')
        
        try:
            with open(json_path, 'r') as f:
                keywords = json.load(f)
            for keyword, color_hex in keywords.items():
                format = QTextCharFormat()
                format.setForeground(QColor(color_hex))  
                self.highlightingRules.append((QRegularExpression(rf'\b{keyword}\b'), format))
                self.colors[keyword] = color_hex
        except FileNotFoundError:
            print(f"colors.json not found at {json_path}")
        except json.JSONDecodeError as e:
            print(f"Error parsing colors.json: {str(e)}")
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            match = pattern.globalMatch(text)
            while match.hasNext():
                m = match.next()
                start = m.capturedStart()
                length = m.capturedLength()
                self.setFormat(start, length, format)
        
        self.highlightFunction(text)
        self.highlightClass(text)
        self.highlightString(text)
        self.highlightNumber(text)
        self.highlightComment(text)
                
    def highlightFunction(self, text):
        function_format = QTextCharFormat()
        function_format.setForeground(QColor(self.colors.get('function', "#FF00FF")))
        function_format.setFontWeight(QFont.Bold)
        function_format.setFontItalic(True)
        function_pattern = QRegularExpression(r'\bdef\b\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(')
        match = function_pattern.globalMatch(text)
        while match.hasNext():
            m = match.next()
            start = m.capturedStart(1)
            length = m.capturedLength(1)
            self.setFormat(start, length, function_format)

    def highlightClass(self, text):
        class_format = QTextCharFormat()
        class_format.setForeground(QColor(self.colors.get('class', "#FF00FF")))
        class_format.setFontWeight(QFont.Bold)
        class_format.setFontItalic(True)
        class_pattern = QRegularExpression(r'\bclass\b\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*')
        match = class_pattern.globalMatch(text)
        while match.hasNext():
            m = match.next()
            start = m.capturedStart(1)
            length = m.capturedLength(1)
            self.setFormat(start, length, class_format)

    def highlightString(self, text):
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(self.colors.get('string', "#00FF00")))
        string_pattern = QRegularExpression(r'".*"')
        match = string_pattern.globalMatch(text)
        while match.hasNext():
            m = match.next()
            start = m.capturedStart()
            length = m.capturedLength()
            self.setFormat(start, length, string_format)

    def highlightNumber(self, text):
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(self.colors.get('number', "#FF0000")))
        number_pattern = QRegularExpression(r'\b\d+\b')
        match = number_pattern.globalMatch(text)
        while match.hasNext():
            m = match.next()
            start = m.capturedStart()
            length = m.capturedLength()
            self.setFormat(start, length, number_format)

    def highlightComment(self, text):
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(self.colors.get('comment', "#0000FF")))
        comment_pattern = QRegularExpression(r'#.*')
        match = comment_pattern.globalMatch(text)
        while match.hasNext():
            m = match.next()
            start = m.capturedStart()
            length = m.capturedLength()
            self.setFormat(start, length, comment_format)

if __name__ == "__main__":
    # This block can be used for testing the SyntaxHighlighter class
    import sys
    from PySide6.QtWidgets import QApplication, QTextEdit

    app = QApplication(sys.argv)
    
    editor = QTextEdit()
    syntax_highlighter = SyntaxHighlighter(editor.document())
    
    test_text = """
def hello_world():
    print("Hello, World!")
    
class MyClass:
    def __init__(self):
        self.value = 42
    
    def my_method(self):
        return self.value * 2
    
if __name__ == "__main__":
    obj = MyClass()
    result = obj.my_method()
    print(result)  # Output: 84
"""
    editor.setText(test_text)
    editor.show()
    sys.exit(app.exec_())