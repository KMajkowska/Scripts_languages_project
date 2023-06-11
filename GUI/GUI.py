from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QMenu, QHBoxLayout, QColorDialog
from PyQt6.QtCore import QCoreApplication, QObject, QSize, Qt
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtGui import QColor
import sys
from GUI_notes_from_archive import NotesArchiveMainWindow
from GUI_active_notes import NotesActiveMainWindow
import os
import importlib

CURRENT_DATABSE_PATH = os.path.join(os.getcwd(),"database\\database.py")


# Ścieżka do pliku notes.py
path_database = CURRENT_DATABSE_PATH

# Załaduj moduł notes
database_spec = importlib.util.spec_from_file_location('database', path_database)
database_moduł = importlib.util.module_from_spec(database_spec)
database_spec.loader.exec_module(database_moduł)

BLUE = "#79DDFF"
PINK = "#FF88EA"
ORANGE = "#FFC288"
WHITE = "#F7F6F6"
RAINBOW = "qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 red, stop: 0.2 orange, stop: 0.4 yellow, stop: 0.6 green, stop: 0.8 blue, stop: 1 violet)"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        getattr(database_moduł, 'main')()


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

        self.color= self.loadBackgroundColor()
        self.openNotes = NotesActiveMainWindow(self.color, self)
        self.archiveNotes = NotesArchiveMainWindow(self.color, self)

        self.buttonOpenNotes = QPushButton("Open notes 🐈", self)
        self.buttonOpenNotes.clicked.connect(lambda: self.openNotes.show())

        self.buttonOpenNotesFromArchive = QPushButton("Open notes from archive 🐁", self)
        self.buttonOpenNotesFromArchive.clicked.connect(lambda: self.archiveNotes.show())

        self.colorButtonsLayout = QHBoxLayout()

        self.blueButton = self.createColorButton(BLUE)
        self.pinkButton = self.createColorButton(PINK)
        self.orangeButton = self.createColorButton(ORANGE)
        self.whiteButton = self.createColorButton(WHITE)
        self.customButton = self.createColorButton(RAINBOW)
        self.customButton.clicked.connect(self.changeCustomColor)
    
        self.colorButtonsLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.layout.addLayout(self.colorButtonsLayout)
        self.layout.addWidget(self.mainLabel)
        self.layout.addWidget(self.buttonOpenNotes)
        self.layout.addWidget(self.buttonOpenNotesFromArchive)

        self.setStyleSheet(create_default_stylesheet())
        self.changeColor(self.color)
        self.openNotes.open_new_note()
    
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
        self.openNotes.color = color
        self.openNotes.change_colors()
        self.archiveNotes.color = color
        self.updateBackgroundColor(color)
    
    def changeCustomColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
           self.changeColor(color.name())

    def loadBackgroundColor(self):
        try:
            with open("background_color.txt", "r") as file:
                color = file.readline().strip()
                background_color = QColor(color).name()
                return background_color
        except FileNotFoundError:
            white = QColor(255, 255, 255)
            return self.updateBackgroundColor(white.name())
        
    def updateBackgroundColor(self, color):
        with open("background_color.txt", "w") as file:
            file.write(color)
            return color
        
def create_default_stylesheet():
    stylesheet = """
        QWidget {
            background-color: white;
        }

        QPlainTextEdit {
            background-color: white;
            border: 3px solid black;
        }

        QLineEdit {
            background-color: white;
            border: 3px solid black;
        }

    """
    return stylesheet



def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
