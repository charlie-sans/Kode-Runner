import PySide6.QtWidgets as QtWidgets
import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
from PySide6.QtGui import QAction
import sys
import json
import asyncio
import websockets

class LineNumberArea(QtWidgets.QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QtCore.QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)

class SyntaxHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlighting_rules = []
        self.load_keywords()

        # Highlight function definitions
        self.add_highlight_rule(r'\bdef\b\s*(\w+)\s*\(', "blue", bold=True)

        # Highlight function calls
        self.add_highlight_rule(r'\b(\w+)\s*(?=\()', "lightblue")

    def load_keywords(self):
        try:
            with open("colors.json", "r") as file:
                keywords = json.load(file)
            for keyword, color in keywords.items():
                self.add_highlight_rule(rf'\b{keyword}\b', color)
        except FileNotFoundError:
            print("colors.json not found.")

    def add_highlight_rule(self, pattern, color, bold=False):
        regex = QtCore.QRegularExpression(pattern)
        format = QtGui.QTextCharFormat()
        format.setForeground(QtGui.QColor(color))
        if bold:
            format.setFontWeight(QtGui.QFont.Bold)
        self.highlighting_rules.append((regex, format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                start = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(start, length, format)

class TextEditor(QtWidgets.QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.line_number_area = LineNumberArea(self)
        self.highlighter = SyntaxHighlighter(self.document())

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_area_width(0)
        self.highlight_current_line()

    def line_number_area_width(self):
        digits = len(str(max(1, self.blockCount())))
        return 3 + self.fontMetrics().horizontalAdvance('9') * digits

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QtCore.QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def line_number_area_paint_event(self, event):
        painter = QtGui.QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QtCore.Qt.darkGray)

        block = self.firstVisibleBlock()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.setPen(QtCore.Qt.white)
                painter.drawText(0, top, self.line_number_area.width(), self.fontMetrics().height(),
                                 QtCore.Qt.AlignRight, str(block.blockNumber() + 1))
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()

    def highlight_current_line(self):
        if not self.isReadOnly():
            selection = QtWidgets.QTextEdit.ExtraSelection()
            line_color = QtGui.QColor(QtCore.Qt.darkGray).lighter(20)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            self.setExtraSelections([selection])

    def highlight_line_with_error(self, line_number):
        if not self.isReadOnly():
            selection = QtWidgets.QTextEdit.ExtraSelection()
            line_color = QtGui.QColor(QtCore.Qt.red).lighter(160)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
            cursor = QtGui.QTextCursor(self.document().findBlockByLineNumber(line_number))
            selection.cursor = cursor
            selection.cursor.clearSelection()
            self.setExtraSelections([selection])

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.auto_indent(event)
        elif event.key() == QtCore.Qt.Key_Backspace:
            self.auto_unindent(event)
        else:
            super().keyPressEvent(event)

    def auto_indent(self, event):
        cursor = self.textCursor()
        block = cursor.block()
        match = QtCore.QRegularExpression(r'^(\s*)').match(block.text())
        cursor.insertText('\n' + match.captured(1))

    def auto_unindent(self, event):
        cursor = self.textCursor()
        block = cursor.block()
        if QtCore.QRegularExpression(r'^\s*$').match(block.text()).hasMatch():
            cursor.removeSelectedText()
        else:
            super().keyPressEvent(event)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text Editor")
        self.setGeometry(100, 100, 800, 600)
        self.editor = TextEditor()
        self.setCentralWidget(self.editor)
        self.editor.setTabStopDistance(4 * self.editor.fontMetrics().horizontalAdvance(' '))
        self.create_menu()
        self.port = 8080  # Default port
        
        import asyncio
        asyncio.set_event_loop(asyncio.new_event_loop())

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        file_menu.addAction(self.create_action('Open', lambda: self.open_file()))
        file_menu.addAction(self.create_action('Save', lambda: self.save_file()))
        file_menu.addAction(self.create_action('Connect to Server', lambda: asyncio.run(self.connect_to_server())))

    def create_action(self, text, slot):
        action = QAction(text, self)
        action.triggered.connect(slot)
        return action

    async def connect_to_server(self):
        try:
            async with websockets.connect(f"ws://localhost:{self.port}") as websocket:
                await websocket.send("Hello Server")
                response = await websocket.recv()
                print(f"Received: {response}")
        except ConnectionRefusedError:
            print("Unable to connect to server. Please make sure the server is running.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def open_file(self):
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                self.editor.setPlainText(file.read())

    def save_file(self):
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.editor.toPlainText())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
