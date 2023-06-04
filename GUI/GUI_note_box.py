from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton
import sys
import os
import importlib.util

# Ścieżka do pliku notes.py
ścieżka_notes = r'C:\Users\karol\OneDrive\Desktop\projekt\notes\notes.py'

# Załaduj moduł notes
notes_spec = importlib.util.spec_from_file_location('notes', ścieżka_notes)
notes_moduł = importlib.util.module_from_spec(notes_spec)
notes_spec.loader.exec_module(notes_moduł)

# Importuj klasę Note
Note = notes_moduł.Note

class Notes(QMainWindow):
    def __init__(self, title, text, time, note):
        super().__init__()

        self.notes = note
        self.title = title
        self.text = text
        self.time = time
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"{self.title} 🦆")
        self.setGeometry(100, 100, 300, 200)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.text_line = QLineEdit()
        self.text_line.setText(f"{self.text}")
        self.time_line = QLineEdit()
        self.time_line.setText(f"{self.time}")

        self.layout.addWidget(self.text_line)
        self.layout.addWidget(self.time_line)

        self.updateNote = QPushButton("Yes, please, update my note! 🐵")
        self.updateNote.clicked.connect(self.updateOpenedNote)

        self.layout.addWidget(self.updateNote)

        self.archiveNote = QPushButton("Yes, please, archive my note! 🦨")
        self.archiveNote.clicked.connect(self.archiveOpenedNote)

        self.layout.addWidget(self.archiveNote)


    def updateOpenedNote(self):
        text_text = self.text_line.text()
        time_text = self.time_line.text()

        self.notes.update(text_text, time_text)

    def archiveOpenedNote(self):
         self.notes.archive()
