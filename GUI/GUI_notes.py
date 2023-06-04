from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QLabel, QDateTimeEdit, QPushButton
import sys
from PyQt6.QtCore import pyqtSlot 
import importlib.util
from GUI_note_box import Notes

# Ścieżka do pliku notes.py
ścieżka_notes = r'C:\Users\karol\OneDrive\Desktop\projekt\notes\notes.py'

# Załaduj moduł notes
notes_spec = importlib.util.spec_from_file_location('notes', ścieżka_notes)
notes_moduł = importlib.util.module_from_spec(notes_spec)
notes_spec.loader.exec_module(notes_moduł)

# Importuj klasę Note
Note = notes_moduł.Note

class NotesMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.notes = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Create note 🦀")
        self.setGeometry(100, 100, 300, 200)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.title_label = QLabel()
        self.title_label.setText("Title")
        self.title = QLineEdit()
        self.text_label = QLabel()
        self.text_label.setText("Text")
        self.text = QLineEdit()
        self.time_label = QLabel()
        self.time_label.setText("Time")
        self.time = QDateTimeEdit()

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.text_label)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.time_label)
        self.layout.addWidget(self.time)

        self.createNote = QPushButton("Yes, right now I want to create new note! 🦔")
        self.createNote.clicked.connect(self.openNotes)
        self.layout.addWidget(self.createNote)

    @pyqtSlot()
    def openNotes(self):
        title_text = self.title.text()
        text_text = self.text.text()
        time_text = self.time.text()
        self.note = Note(-1, title_text, text_text, time_text, True)
        self.notesWindow = Notes(title_text, text_text, time_text, self.note)
        self.notesWindow.show()

