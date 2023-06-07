from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QListWidgetItem,QMessageBox, QPushButton,QLineEdit, QDateTimeEdit, QListView, QListWidget, QHBoxLayout, QPlainTextEdit, QAbstractItemView
from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSlot 
from PyQt6.QtGui import QFont, QPalette, QColor
import importlib.util
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from functions import CURRENT_NOTES_PATH
from functions import speech_to_text


# Ścieżka do pliku notes.py
ścieżka_notes = CURRENT_NOTES_PATH

# Załaduj moduł notes
notes_spec = importlib.util.spec_from_file_location('notes', ścieżka_notes)
notes_moduł = importlib.util.module_from_spec(notes_spec)
notes_spec.loader.exec_module(notes_moduł)

# Importuj klasę Note
Note = notes_moduł.Note
class NotesActiveMainWindow(QMainWindow):
    def __init__(self, color, main):
        super().__init__()
        self.main = main
        self.database = None
        self.color = color
        self.notes = []
        self.notes_list_widget = QListWidget()
        self.current_note = None
       
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Open notes 🦎")
        self.setGeometry(100, 100, 300, 200)

        self.open_database()
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.mainLabel = QLabel()
        self.mainLabel.setText("Now you can choose your note, are you happy? \nJust click on the note, and it will open! 🐢")

        self.layout.addWidget(self.mainLabel)
        self.notes_layout = QHBoxLayout()
        self.notes_layout.setContentsMargins(0, 0, 0, 0)
        #self.centralWidget.setLayout(self.notes_layout)

     
        self.notes_list_widget.currentRowChanged.connect(self.select_note)
        self.notes_layout.addWidget(self.notes_list_widget)

       
        self.create_note_editor()
        self.create_new_note_button()
        self.layout.addLayout(self.notes_layout)
        
    def load_active_notes(self):
        query = QSqlQuery()
        query.prepare("SELECT * FROM Notes WHERE active = 1")
        query.exec()

        while query.next():
            uid = query.value(0)
            title = query.value(1)
            text = query.value(2)
            time = query.value(3)
            last_edit = query.value(4)
            active = query.value(5)
            note = Note(uid, title, text, time, last_edit, active)
            self.notes.append(note)
            self.add_note_to_list(note)

    def open_database(self):
        self.database = QSqlDatabase.addDatabase("QSQLITE")
        self.database.setDatabaseName('NotesDatabase.sqlite3')
 
        if not self.database.open():
            self.mainLabel.setText("Database is not open")
            return False
        self.load_active_notes()

        return True
    
    def create_note_editor(self):
        self.editor_layout = QVBoxLayout()

        self.note_title = QLineEdit()
        self.note_title.setStyleSheet(f"background-color: {self.color}; opacity: 0.2;")
        self.note_title.setReadOnly(True)

        self.note_content = QPlainTextEdit()
        self.note_content.setStyleSheet(f"border: 3px solid dark; background-color: {self.color}; opacity: 0.2;")
        self.note_title.setReadOnly(True)

        self.edit_button = QPushButton("Edit 🐞")
        self.edit_button.clicked.connect(self.edit_note)

        self.save_button = QPushButton("Save 🐿️")
        self.save_button.clicked.connect(self.save_note)

        self.delete_button = QPushButton("Delete 🦫")
        self.delete_button.clicked.connect(self.delete_note)

        self.archive_button = QPushButton("Archive 🐼")
        self.archive_button.clicked.connect(self.archive_note)

        self.transcribe_button = QPushButton("Transcribe 🎵🦜")
        self.transcribe_button.clicked.connect(self.transcribe_text)
        

        self.editor_layout.addWidget(self.note_title)
        self.editor_layout.addWidget(self.note_content)
        self.editor_layout.addWidget(self.edit_button)
        self.editor_layout.addWidget(self.save_button)
        self.editor_layout.addWidget(self.delete_button)
        self.editor_layout.addWidget(self.archive_button)
        self.editor_layout.addWidget(self.transcribe_button)

        self.notes_layout.addLayout(self.editor_layout)


    def create_new_note_button(self):
        self.new_note_button = QPushButton("Create new Note")
        self.new_note_button.clicked.connect(self.open_new_note)
        self.notes_layout.addWidget(self.new_note_button)

    def add_note_to_list(self, note):
        item_text = self.get_item_note_text(note)
        list_item = QListWidgetItem(item_text)
        font = QFont()
        font.setBold(True)
        list_item.setFont(font)

        self.notes_list_widget.addItem(list_item)

    def update_note_in_list(self, index, note):
        item_text = self.get_item_note_text(note)
        self.notes_list_widget.item(index).setText(item_text)

    def get_item_note_text(self, note):
        first_line= note.getText().partition('\n')[0]
        if len(first_line) < 100:
            preview = first_line if first_line else ''
        else:
            preview = first_line[0:100] + "..."
        item_text = f"{note.getTitle()}\n{preview}\n{note.getLastEdit()}"
        return item_text
   
    def select_note(self, index):
        if index >= 0 and index < len(self.notes):
            self.current_note = self.notes[index]
            self.note_title.setText(self.current_note.getTitle())
            self.note_content.setPlainText(self.current_note.getText())
            self.note_title.setReadOnly(True)
            self.note_content.setReadOnly(True)

    def edit_note(self):
        if self.current_note:
            self.note_title.setReadOnly(False)
            self.note_content.setReadOnly(False)
            self.note_title.setFocus()
            self.note_content.setFocus()

    def delete_note(self):
        if self.current_note is not None:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Confirmation")
            msg_box.setText("Are you sure you want to delete the note? You won't be able to access it anymore.")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg_box.setDefaultButton(QMessageBox.StandardButton.No)

            response = msg_box.exec()
            
            if response == QMessageBox.StandardButton.Yes:
                self.notes.remove(self.current_note)
                self.notes_list_widget.takeItem(self.notes_list_widget.currentRow())
                self.current_note.deleteFromDatabase()
                self.current_note=None
                self.clear_editor()
           
                print("Note deleted")
            else:
                print("Deletion cancelled")
            

    def archive_note(self):
        if self.current_note is not None:
            self.current_note.archive()
            self.main.archiveNotes.load_archive_notes()
            self.notes.remove(self.current_note)
            self.notes_list_widget.takeItem(self.notes_list_widget.currentRow())
            self.clear_editor()
            

    def clear_editor(self):
        self.current_note = None
        self.note_title.setText("")
        self.note_content.setPlainText("")
        self.notes_list_widget.clearSelection()

    def open_new_note(self):
        self.clear_editor()
        self.note_title.setPlaceholderText("Write your note title here")
        self.note_content.setPlaceholderText("Here you can write the text for your perfect note!")
        self.note_title.setReadOnly(False)
        self.note_content.setReadOnly(False)
        self.current_note=None

    def create_new_note(self):
        title = self.note_title.text()
        text = self.note_content.toPlainText()
        time = QDateTimeEdit()
        time.setDateTime(QDateTime.currentDateTime())
        time.setDisplayFormat("dd-MM-yyyy HH:mm:ss")
        time = time.text()
        last_edit = time
        note = Note(-1, title, text, time, last_edit, True)
        self.current_note = note
        note.addToDatabase()
        self.notes.append(note)
        self.add_note_to_list(note)
        self.notes_list_widget.setCurrentRow(self.notes_list_widget.currentIndex().row()+1)
    

    def save_note(self):
        if self.current_note is not None:
            new_title = self.note_title.text()
            new_text = self.note_content.toPlainText()
            last_edit = QDateTimeEdit()
            last_edit.setDateTime(QDateTime.currentDateTime())
            last_edit.setDisplayFormat("dd-MM-yyyy HH:mm:ss")
            last_edit = last_edit.text()
            self.current_note.update(new_title, new_text, self.current_note.getTime(), last_edit)
            index = self.notes_list_widget.currentIndex().row()
            self.notes[index] = self.current_note
            self.update_note_in_list(index, self.current_note)
        else:
            self.create_new_note()
    
    def transcribe_text(self):
        try:
            text = speech_to_text()
            self.note_content.appendPlainText(text)
        except ValueError: pass


    
    
