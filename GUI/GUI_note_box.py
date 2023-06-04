from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QLabel
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
        note.addToDatabase()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"{self.title} 🦆")
        self.setGeometry(100, 100, 300, 200)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.text_label = QLabel()
        self.text_label.setText(f"{self.text}")
        self.time_label = QLabel()
        self.time_label.setText(f"{self.time}")

        self.layout.addWidget(self.text_label)
        self.layout.addWidget(self.time_label)
