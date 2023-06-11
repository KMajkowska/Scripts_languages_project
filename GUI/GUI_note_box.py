from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QPlainTextEdit
import sys
import os
import importlib.util
from functions import CURRENT_NOTES_PATH

# Ścieżka do pliku notes.py
ścieżka_notes = CURRENT_NOTES_PATH

# Załaduj moduł notes
notes_spec = importlib.util.spec_from_file_location('notes', ścieżka_notes)
notes_moduł = importlib.util.module_from_spec(notes_spec)
notes_spec.loader.exec_module(notes_moduł)

# Importuj klasę Note
Note = notes_moduł.Note

class Notes(QMainWindow):
    def __init__(self, title, text, time, last_edit, note, archive):
        super().__init__()

        self.note = note
        self.title = title
        self.text = text
        self.last_edit = last_edit
        self.time = time
        self.archive = archive
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"{self.title} 🦆")
        self.setGeometry(100, 100, 300, 200)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.title_line = QLineEdit()
        self.title_line.setText(f"{self.title}")
        self.title_line.setReadOnly(True)
        self.text_line = QPlainTextEdit()
        self.text_line.setPlainText(f"{self.text}")
        self.text_line.setReadOnly(True)

        self.layout.addWidget(self.title_line)
        self.layout.addWidget(self.text_line)
        

        self.retrieveNote = QPushButton("Yes, please, retrieve my note! 🐵")
        self.retrieveNote.clicked.connect(self.retrieveOpenedNote)

        self.layout.addWidget(self.retrieveNote)
        
        self.deleteNote = QPushButton("Yes, please, delete my note! 🦨")
        self.deleteNote.clicked.connect(self.deleteOpenedNote)

        self.layout.addWidget(self.deleteNote)

    def retrieveOpenedNote(self):
        self.archive.deleteNote()
        self.note.update(self.title, self.text, self.time, self.last_edit, self.note.getReminder())
        self.archive.main.openNotes.add_new_note_to_list(self.note)
        #self.archive.load_archive_notes()
        self.close()


    def deleteOpenedNote(self):
         self.archive.deleteNote()
         self.note.deleteFromDatabase()
         self.close()
