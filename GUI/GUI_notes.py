from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QLabel, QDateTimeEdit, QPushButton, QPlainTextEdit
import sys
from PyQt6.QtCore import pyqtSlot, QDateTime 
import importlib.util
from GUI_note_box import Notes
from functions import CURRENT_NOTES_PATH, speech_to_text

# Ścieżka do pliku notes.py
ścieżka_notes = CURRENT_NOTES_PATH

# Załaduj moduł notes
notes_spec = importlib.util.spec_from_file_location('notes', ścieżka_notes)
notes_moduł = importlib.util.module_from_spec(notes_spec)
notes_spec.loader.exec_module(notes_moduł)

# Importuj klasę Note
Note = notes_moduł.Note

class NotesMainWindow(QMainWindow):
    def __init__(self, color):
        super().__init__()
        self.color = color
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
        self.text = QPlainTextEdit()    #PlainTextEdit zamiast LineEdit żeby można było w kilku linijkach pisać notatkę
        self.time_label = QLabel()
        self.time_label.setText("Time")
        self.time = QDateTimeEdit()
        self.time.setDateTime(QDateTime.currentDateTime())
        self.time.setDisplayFormat("dd-MM-yyyy HH:mm:ss")
        self.time.setReadOnly(True)

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.text_label)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.time_label)
        self.layout.addWidget(self.time)

        
        self.transcribe_button = QPushButton("Transcribe 🎵🦜")
        self.transcribe_button.clicked.connect(self.transcribe_text)
        
        self.layout.addWidget(self.transcribe_button)

        self.createNote = QPushButton("Yes, right now I want to create new note! 🦔")
        self.createNote.clicked.connect(lambda: self.openNotes(self.color))
        self.layout.addWidget(self.createNote)


    def transcribe_text(self):
        try:
            text = speech_to_text()
            self.text.appendPlainText(text)
        except ValueError: pass

    @pyqtSlot()
    def openNotes(self, color):
        title_text = self.title.text()
        text_text = self.text.toPlainText()
        time_text = self.time.text()
        self.note = Note(-1, title_text, text_text, time_text, True)
        self.notesWindow = Notes(title_text, text_text, time_text, self.note)
        self.notesWindow.setStyleSheet(f"background-color: {color};")
        self.notesWindow.show()

