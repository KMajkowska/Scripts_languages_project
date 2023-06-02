from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import QCoreApplication, QObject
from PyQt6.QtCore import pyqtSlot 
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import sys
from GUI_notes import NotesMainWindow
from GUI_notes_from_archive import NotesArchiveMainWindow
from GUI_active_notes import NotesActiveMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Main Window 🦄")
        self.setGeometry(100, 100, 300, 200)

        self.notesWindow = None 
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.mainLabel = QLabel()
        self.mainLabel.setText("Welcome to our app, which can manage your notes! 🐸 ")

        self.buttonOpenNotes = QPushButton("Open notes 🐈", self)
        self.buttonOpenNotes.clicked.connect(self.openNotes)

        self.buttonNewNotes = QPushButton("New notes 🐧", self)
        self.buttonNewNotes.clicked.connect(self.openNotes)

        self.buttonOpenNotesFromArchive = QPushButton("Open notes from archive 🦜", self)
        self.buttonOpenNotesFromArchive.clicked.connect(self.openNotesFromArchive)

        self.layout.addWidget(self.mainLabel)
        self.layout.addWidget(self.buttonOpenNotes)
        self.layout.addWidget(self.buttonNewNotes)
        self.layout.addWidget(self.buttonOpenNotesFromArchive)

    @pyqtSlot()
    def openNotes(self):
        if self.notesWindow is None:  
            self.notesWindow = NotesActiveMainWindow()
        self.notesWindow.show()

    @pyqtSlot()
    def openNotesFromArchive(self):
        if self.notesWindow is None:  
            self.notesWindow = NotesArchiveMainWindow()
        self.notesWindow.show()

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()