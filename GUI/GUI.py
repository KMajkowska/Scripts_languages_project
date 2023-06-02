from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import QCoreApplication, QObject
from PyQt6.QtCore import pyqtSlot 
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import sys
from GUI_notes import NotesMainWindow
import importlib.util

# Ścieżka do pliku notes.py
database_path = r'C:\Users\karol\OneDrive\Desktop\projekt\database\database.py'

# Załaduj moduł notes
database_spec = importlib.util.spec_from_file_location('databse', database_path)
database_module = importlib.util.module_from_spec(database_spec)
database_spec.loader.exec_module(database_module)

# Importuj klasę Note
NoteDatabase = database_module.NotesDatabase

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 300, 200)

        self.notesWindow = None  # Inicjalizacja obiektu NotesMainWindow jako atrybut klasy

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.mainLabel = QLabel()
        self.mainLabel.setText("Welcome to our app, which manage your notes! 🐸 ")

        self.buttonOpenNotes = QPushButton("Open notes 🐈", self)
        self.buttonOpenNotes.clicked.connect(self.openNotes)

        self.buttonNewNotes = QPushButton("New notes 🐧", self)
        self.buttonNewNotes.clicked.connect(self.openNotes)

        self.buttonOpenNotesFromArchive = QPushButton("Open notes from archive 🦜", self)
        self.buttonOpenNotesFromArchive.clicked.connect(self.open_database)

        self.layout.addWidget(self.mainLabel)
        self.layout.addWidget(self.buttonOpenNotes)
        self.layout.addWidget(self.buttonNewNotes)
        self.layout.addWidget(self.buttonOpenNotesFromArchive)

    @pyqtSlot()
    def openNotes(self):
        if self.notesWindow is None:  # Sprawdzenie, czy obiekt NotesMainWindow nie został już utworzony
            self.notesWindow = NotesMainWindow()
        self.notesWindow.show()

    def open_database(self):
        self.database = QSqlDatabase.addDatabase("QSQLITE")
        self.database.setDatabaseName('NotesDatabase')

        if not self.database.open():
            self.result_label.setText("Nie udało się otworzyć bazy danych.")
            return False

        return True
    

    def close_database(self):
        self.database.close()


def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()