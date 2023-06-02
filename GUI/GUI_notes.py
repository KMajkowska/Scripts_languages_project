from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QListWidget, QHBoxLayout, QPushButton, QDateTimeEdit, QLabel, QLineEdit, QFileDialog, QListWidgetItem
import sys
import importlib.util

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

        self.notes = Note()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Notes Main Window 🦀")
        self.setGeometry(100, 100, 300, 200)