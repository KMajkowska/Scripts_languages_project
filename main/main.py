import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QTextEdit, QWidgetAction, QFileDialog


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        self.initMenuBar()

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Text Editor")
        self.show()

    def initMenuBar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")

        new_action = QWidgetAction("New", self)
        new_action.triggered.connect(self.newFile)
        file_menu.addAction(new_action)

        open_action = QWidgetAction("Open", self)
        open_action.triggered.connect(self.openFile)
        file_menu.addAction(open_action)

        save_action = QWidgetAction("Save", self)
        save_action.triggered.connect(self.saveFile)
        file_menu.addAction(save_action)

    def newFile(self):
        self.textEdit.clear()

    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt)", options=options)

        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.textEdit.setPlainText(content)

    def saveFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt)", options=options)

        if file_path:
            with open(file_path, "w") as file:
                content = self.textEdit.toPlainText()
                file.write(content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = TextEditor()
    sys.exit(app.exec_())