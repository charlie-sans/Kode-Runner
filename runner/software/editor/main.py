import PySide6.QtWidgets as QtWidgets
import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import sys

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

        # Define your keywords and their respective colors
        keywords = {
            'def': QtGui.QColor(QtCore.Qt.blue),
            'class': QtGui.QColor(QtCore.Qt.darkMagenta),
            'import': QtGui.QColor(QtCore.Qt.darkCyan),
            'from': QtGui.QColor(QtCore.Qt.darkCyan),
            'self': QtGui.QColor(QtCore.Qt.darkRed),
            'return': QtGui.QColor(QtCore.Qt.darkGreen),
            'if': QtGui.QColor(QtCore.Qt.darkYellow),
            'else': QtGui.QColor(QtCore.Qt.darkYellow),
            'while': QtGui.QColor(QtCore.Qt.darkYellow),
            'for': QtGui.QColor(QtCore.Qt.darkYellow),
            'in': QtGui.QColor(QtCore.Qt.darkYellow),
            'True': QtGui.QColor(QtCore.Qt.darkBlue),
            'False': QtGui.QColor(QtCore.Qt.darkBlue),
            'None': QtGui.QColor(QtCore.Qt.darkBlue),
        }

        for keyword, color in keywords.items():
            pattern = QtCore.QRegularExpression(f'\\b{keyword}\\b')
            format = QtGui.QTextCharFormat()
            format.setForeground(color)
            self.highlighting_rules.append((pattern, format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

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
        digits = 1
        max_block = max(1, self.blockCount())
        while max_block >= 10:
            max_block //= 10
            digits += 1
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

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
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QtCore.Qt.white)
                painter.drawText(0, top, self.line_number_area.width(), self.fontMetrics().height(),
                                 QtCore.Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def highlight_current_line(self):
        extra_selections = []

        if not self.isReadOnly():
            selection = QtWidgets.QTextEdit.ExtraSelection()
            line_color = QtGui.QColor(QtCore.Qt.darkGray).lighter(160)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Text Editor")
        self.setGeometry(100, 100, 800, 600)
        
        self.code_ws = None
        self.endpoints = {
            "code": "ws://localhost:5000/code",
            "PMS": "ws://localhost:5000/PMS"
        }
        self.port = None


        self.editor = TextEditor()
        self.setCentralWidget(self.editor)

        self.create_menu()
 

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        open_action = QtGui.QAction('Open', self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QtGui.QAction('Save', self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        connect_action = QtGui.QAction('Connect to Server', self)
        connect_action.triggered.connect(self.connect_to_server)
        file_menu.addAction(connect_action)

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
                
    def connect_to_server(self):
        with open("config.json", "r") as file:
            config = json.load(file)
            self.server = config["server"]
            self.port = config["port"]
   
            self.code_ws = websockets.connect(f"ws://{self.server}:{self.port}/code")
            self.PMS_ws = websockets.connect(f"ws://{self.server}:{self.port}/PMS")
            
    def set_style(self, style):
        with open(style, 'r') as file:
            self.setStyleSheet(file.read())

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    editor = MainWindow()
    editor.show()
    sys.exit(app.exec())