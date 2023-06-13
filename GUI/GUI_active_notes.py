from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import QMainWindow,QComboBox, QLabel, QVBoxLayout, QWidget, QListWidgetItem,QMessageBox, QSizePolicy, QPushButton,QLineEdit, QDateTimeEdit, QListView, QListWidget, QHBoxLayout, QPlainTextEdit, QAbstractItemView
from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSlot 
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor
import importlib.util
import os
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from functions import CURRENT_NOTES_PATH
from functions import speech_to_text, get_emoji_list
from datetime import datetime, timedelta


# Ścieżka do pliku notes.py
ścieżka_notes = CURRENT_NOTES_PATH
BASE_DIR = os.path.join(os.getcwd())

# Załaduj moduł notes
notes_spec = importlib.util.spec_from_file_location('notes', ścieżka_notes)
notes_moduł = importlib.util.module_from_spec(notes_spec)
notes_spec.loader.exec_module(notes_moduł)

# Importuj klasę Note
Note = notes_moduł.Note
class NotesActiveMainWindow(QMainWindow):

    reminder_added = pyqtSignal(Note)
    def __init__(self, color, main):
        super().__init__()
        self.main = main
        self.database = None
        self.color = color
        self.notes = []
        self.filtered = []
        self.notes_list_widget = QListWidget()
        self.filtered_notes = QListWidget()
        self.current_note = None
        self.reminder = datetime(2000, 1, 1, 0, 0)

       
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

        self.notes_list_widget.currentRowChanged.connect(self.select_note)
        self.notes_list_widget.setFixedWidth(200)
        self.notes_layout.addWidget(self.notes_list_widget)

        self.create_note_editor()
        self.filtered_notes.currentRowChanged.connect(self.select_filtered_note)
        self.filtered_notes.setFixedWidth(200)
        self.notes_layout.addWidget(self.filtered_notes)
        self.layout.addLayout(self.notes_layout)
        

        
    def load_active_notes(self):
        query = QSqlQuery()
        query.prepare("SELECT * FROM Notes WHERE active = 1")
        query.exec()

        query.last()

        while query.isValid():
            uid = query.value(0)
            title = query.value(1)
            text = query.value(2)
            time = query.value(3)
            last_edit = query.value(4)
            active = query.value(5)
            reminder = query.value(6)
            note = Note(uid, title, text, time, last_edit, active, reminder)
            self.add_note_to_list(note)

            query.previous()

    def load_filtered_notes(self):
        current_datetime = datetime.now()
        time = datetime.strftime(current_datetime, "%Y-%m-%d %H:%M:%S.%f")
        query = QSqlQuery()
        query.prepare("SELECT * FROM Notes WHERE reminder >= :current_datetime")
        query.bindValue(":current_datetime", time)
        query.exec()

        while query.next():
            uid = query.value(0)
            title = query.value(1)
            text = query.value(2)
            time = query.value(3)
            last_edit = query.value(4)
            active = query.value(5)
            reminder = query.value(6)
            note = Note(uid, title, text, time, last_edit, active, reminder)
            self.add_note_to_filtered_list(note)
        
    def open_database(self):
        self.database = QSqlDatabase.addDatabase("QSQLITE")
        self.database.setDatabaseName('NotesDatabase.sqlite3')

        if not self.database.open():
            self.mainLabel.setText("Database is not open")
            return False

        self.load_active_notes()
        self.load_filtered_notes()

        return True
    
    def create_note_editor(self):

        self.editor_layout = QVBoxLayout()
        self.note_title = QLineEdit()
        self.note_content = QPlainTextEdit()
        self.reminder_content = QLineEdit()

        self.emoji_combobox = QComboBox()
        emoji_list = get_emoji_list()
        self.emoji_combobox.addItems(emoji_list)
        self.emoji_combobox.currentTextChanged.connect(self.add_emoji_to_note)

        self.note_reminder = QDateTimeEdit()

        self.note_reminder.setDisplayFormat("MMM dd hh:mm:ss")
        self.note_reminder.setDateTime(QDateTime.currentDateTime())
        self.note_title.setReadOnly(True)

        self.new_note_button = QPushButton("Create new note 🐇")
        self.new_note_button.clicked.connect(self.open_new_note)
        
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

        self.reminder_button = QPushButton("Reminder 🐘")
        self.reminder_button.clicked.connect(self.reminder_note)

        self.txt_button = QPushButton("Save as txt file 🐛")
        self.txt_button.clicked.connect(self.save_as_txt)

        self.reminder_added.connect(self.add_note_to_filtered_list)

        button_layout1 = QHBoxLayout()
        button_layout1.addWidget(self.new_note_button)
        button_layout1.addWidget(self.edit_button)

        button_layout2 = QHBoxLayout()
        button_layout2.addWidget(self.save_button)
        button_layout2.addWidget(self.delete_button)

        button_layout3 = QHBoxLayout()
        button_layout3.addWidget(self.archive_button)
        button_layout3.addWidget(self.reminder_button)
        
        button_layout4 = QHBoxLayout()
        button_layout4.addWidget(self.txt_button)
        button_layout4.addWidget(self.transcribe_button)

        
        self.editor_layout.addWidget(self.note_title)
        self.editor_layout.addWidget(self.note_content)
        self.editor_layout.addWidget(self.reminder_content)
        self.editor_layout.addWidget(self.note_reminder)

        self.editor_layout.addLayout(button_layout1)
        self.editor_layout.addLayout(button_layout2)
        self.editor_layout.addLayout(button_layout3)
        self.editor_layout.addLayout(button_layout4)
        self.editor_layout.addWidget(self.emoji_combobox)

        self.notes_layout.addLayout(self.editor_layout)

    def add_emoji_to_note(self, emoji):
        cursor = self.note_content.textCursor()
        cursor.insertText(emoji)
        self.note_content.setFocus()

    def reminder_note(self):
        q_note_remind = self.note_reminder.dateTime()
        self.reminder = q_note_remind.toPyDateTime()


    def add_note_to_filtered_list(self, note):
        item_text = self.get_item_note_text(note)
        list_item = QListWidgetItem(item_text)
        font = QFont()
        font.setBold(True)
        list_item.setFont(font)
        self.filtered.append(note)
        self.filtered_notes.addItem(list_item)

    def add_new_note_to_filtered_list(self, note):
        item_text = self.get_item_note_text(note)
        list_item = QListWidgetItem(item_text)
        font = QFont()
        font.setBold(True)
        list_item.setFont(font)
        self.filtered.insert(0, note)
        self.filtered_notes.insertItem(0,list_item)

    def add_note_to_list(self, note):
        item_text = self.get_item_note_text(note)
        list_item = QListWidgetItem(item_text)
        font = QFont()
        font.setBold(True)
        list_item.setFont(font)
        self.notes.append(note)
        self.notes_list_widget.addItem(list_item)

    def add_new_note_to_list(self, note):
        item_text = self.get_item_note_text(note)
        list_item = QListWidgetItem(item_text)
        font = QFont()
        font.setBold(True)
        list_item.setFont(font)
        self.notes.insert(0, note)
        self.notes_list_widget.insertItem(0,list_item)

    def update_note_in_list(self, index, note):
        item_text = self.get_item_note_text(note)
        if index >= 0 and index < self.notes_list_widget.count():
            self.notes_list_widget.item(index).setText(item_text)

    def update_note_filtered_list(self, index, note):
        item_text = self.get_item_note_text(note)
        if str(note.getReminder()) >= str(datetime.now()):
           if index >= 0 and index < self.filtered_notes.count():
                self.filtered_notes.item(index).setText(item_text)       


    def get_item_note_text(self, note):
        first_line = note.getText().partition('\n')[0]
        if len(first_line) < 20:
            preview = first_line if first_line else ''
        else:
            preview = first_line[:20] + "..."
        item_text = f"{note.getTitle()}\n{preview}\n{note.getLastEdit()}"
        return item_text
   
    def select_note(self, index):
        self.filtered_notes.clearSelection()
        self.current_note = None
        if index >= 0 and index < len(self.notes):
            self.current_note = self.notes[index]
            self.note_title.setText(self.current_note.getTitle())
            if str(self.current_note.getReminder()) == str(self.reminder):
                self.note_content.setPlainText(self.current_note.getText())
                self.reminder_content.setText("No reminder set")
            else:
                self.note_content.setPlainText(self.current_note.getText())
                self.reminder_content.setText("REMINDER: " + str(self.current_note.getReminder()))
            self.note_title.setReadOnly(True)
            self.note_content.setReadOnly(True)
        

    def select_filtered_note(self, index):
        self.notes_list_widget.clearSelection()
        self.current_note = None
        if index >= 0 and index < len(self.filtered):
            self.current_note = self.filtered[index]
            self.note_title.setText(self.current_note.getTitle())
            self.note_content.setPlainText(self.current_note.getText())
            self.reminder_content.setText("REMINDER: " + str(self.current_note.getReminder()))
            self.note_title.setReadOnly(True)
            self.note_content.setReadOnly(True)

    def edit_note(self):
        if self.current_note is not None:
            self.reminder= self.current_note.getReminder()
            self.note_title.setReadOnly(False)
            self.note_content.setReadOnly(False)
            self.note_title.setFocus()
            self.note_content.setFocus()

    def save_as_txt(self):
        if self.current_note is not None:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Note As", "", "Text Files (*.txt)")

            if file_path:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.current_note.getText())
                    if(str(self.current_note.getReminder()) > str(datetime(2000, 1, 1, 0, 0))):
                        file.write('\n' + self.current_note.getReminder())


    def delete_note(self):
        if self.current_note is not None:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Confirmation")
            msg_box.setText("Are you sure you want to delete the note? You won't be able to access it anymore.")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            msg_box.setDefaultButton(QMessageBox.StandardButton.No)
            msg_box.setStyleSheet(f"background-color: {self.color};")
            response = msg_box.exec()
            
            if response == QMessageBox.StandardButton.Yes:
                self.current_note.deleteFromDatabase()
                self.notes.remove(self.current_note)
                self.notes_list_widget.takeItem(self.notes_list_widget.currentRow())
                self.current_note=None
                self.open_new_note()
                
           
                print("Note deleted")
            else:
                print("Deletion cancelled")
            

    def archive_note(self):
        if self.current_note is not None:
            self.current_note.archive()
            self.main.archiveNotes.load_archive_notes()
            self.notes.remove(self.current_note)
            self.notes_list_widget.takeItem(self.notes_list_widget.currentRow())
            self.open_new_note()
            

    def clear_editor(self):
        self.note_title.setText("")
        self.note_content.setPlainText("")
        self.notes_list_widget.clearSelection()
        self.notes_list_widget.setCurrentRow(-1)

    def open_new_note(self):
        self.clear_editor()
        self.note_title.setPlaceholderText("Write your note title here")
        self.note_content.setPlaceholderText("Here you can write the text for your perfect note!")
        self.reminder_content.setPlaceholderText("Here your reminder will be shown!")
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
        note = Note(-1, title, text, time, last_edit, True, self.reminder)
        self.current_note = note
        note.addToDatabase()
        self.add_new_note_to_list(note)
        self.notes_list_widget.setCurrentRow(0)
        time = datetime.now()
        if(str(self.current_note.getReminder()) >= str(time)):
            self.add_new_note_to_filtered_list(note)
            self.filtered_notes.setCurrentRow(0)
    

    def save_note(self):
        if self.current_note is not None:
            new_title = self.note_title.text()
            new_text = self.note_content.toPlainText()
            last_edit = QDateTimeEdit()
            last_edit.setDateTime(QDateTime.currentDateTime())
            last_edit.setDisplayFormat("dd-MM-yyyy HH:mm:ss")
            last_edit = last_edit.text()
            self.current_note.setReminder(self.reminder)
            self.current_note.update(new_title, new_text, self.current_note.getTime(), last_edit, self.current_note.getReminder())
            if str(self.current_note.getReminder()) >= str(datetime(2000, 1, 1, 0, 0)): 
                index = self.filtered_notes.currentIndex().row()
                self.filtered[index] = self.current_note
                self.update_note_filtered_list(index, self.current_note)
                index = self.notes_list_widget.currentIndex().row()
                self.notes[index] = self.current_note
                self.update_note_in_list(index, self.current_note)
            else:
                index = self.notes_list_widget.currentIndex().row()
                self.notes[index] = self.current_note
                self.update_note_in_list(index, self.current_note)
            self.reminder = datetime(2000, 1, 1, 0, 0)
        else:
            self.create_new_note()
            self.reminder = datetime(2000, 1, 1, 0, 0)

    def transcribe_text(self):
        try:
            text = speech_to_text()
            self.note_content.appendPlainText(text)
        except ValueError: pass


    def change_colors(self):
        styleSheet = """
            QPushButton {
                background-color: rgba(0, 0, 0, 40);
                border: 1px solid rgba(0, 0, 0, 50);
                padding: 5px;} 
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 100);}"
        """
        background ="background-color: rgba(255, 255, 255, 150);" 
        self.note_title.setStyleSheet(background)
        self.note_content.setStyleSheet(background)
        self.emoji_combobox.setStyleSheet(background)
        self.note_reminder.setStyleSheet(background)
        self.reminder_content.setStyleSheet(background)
        self.new_note_button.setStyleSheet(styleSheet)
        self.edit_button.setStyleSheet(styleSheet)
        self.save_button.setStyleSheet(styleSheet)
        self.delete_button.setStyleSheet(styleSheet)
        self.archive_button.setStyleSheet(styleSheet)
        self.transcribe_button.setStyleSheet(styleSheet)
        self.reminder_button.setStyleSheet(styleSheet)
        self.txt_button.setStyleSheet(styleSheet)
        self.main.buttonOpenNotes.setStyleSheet(styleSheet)
        self.main.buttonOpenNotesFromArchive.setStyleSheet(styleSheet)
        self.notes_list_widget.setStyleSheet("""
                                             QListWidget::item { border: 1px solid rgba(0, 0, 0, 120);
                                              background-color: rgba(255, 255, 255, 90); }
                                             QListWidget::item:selected { color: rgba(0, 0, 0, 120); }"
                                             """)
