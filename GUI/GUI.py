from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QMenu, QHBoxLayout
from PyQt6.QtCore import QCoreApplication, QObject, QSize, Qt
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import sys
from GUI_notes import NotesMainWindow
from GUI_notes_from_archive import NotesArchiveMainWindow
from GUI_active_notes import NotesActiveMainWindow


BLUE = "#79DDFF"
PINK = "#FF88EA"
ORANGE = "#FFC288"
WHITE = "#F7F6F6"

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

        self.openNotes = NotesActiveMainWindow(WHITE)
        self.newNotes = NotesMainWindow(WHITE)
        self.archiveNotes = NotesArchiveMainWindow(WHITE)

        self.buttonOpenNotes = QPushButton("Open notes 🐈", self)
        self.buttonOpenNotes.clicked.connect(lambda: self.openNotes.show())
        
        self.buttonNewNotes = QPushButton("New notes 🐧", self)
        self.buttonNewNotes.clicked.connect(lambda: self.newNotes.show())

        self.buttonOpenNotesFromArchive = QPushButton("Open notes from archive 🐁", self)
        self.buttonOpenNotesFromArchive.clicked.connect(lambda: self.archiveNotes.show())

        self.colorButtonsLayout = QHBoxLayout()

        self.blueButton = self.createColorButton(BLUE)
        self.pinkButton = self.createColorButton(PINK)
        self.orangeButton = self.createColorButton(ORANGE)
        self.whiteButton = self.createColorButton(WHITE)
    
        self.colorButtonsLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.layout.addLayout(self.colorButtonsLayout)
        self.layout.addWidget(self.mainLabel)
        self.layout.addWidget(self.buttonOpenNotes)
        self.layout.addWidget(self.buttonNewNotes)
        self.layout.addWidget(self.buttonOpenNotesFromArchive)
    
    def createColorButton(self, color):
        button = QPushButton()
        button.setFixedSize(QSize(25, 25))
        button.setStyleSheet(f"border : 2px solid black; background-color : {color}")
        self.colorButtonsLayout.addWidget(button)
        button.clicked.connect(lambda: self.changeColor(color))
        return button
    
    def changeColor(self, color):
        self.setStyleSheet(f"background-color: {color};")
        self.openNotes.setStyleSheet(f"background-color: {color};")
        self.archiveNotes.setStyleSheet(f"background-color: {color};")
        self.newNotes.setStyleSheet(f"background-color: {color};")
        self.openNotes.color = color
        self.archiveNotes.color = color
        self.newNotes.color = color



def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()