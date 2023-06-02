from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QWidget, QComboBox, QStyledItemDelegate, QTableView
from PyQt6.QtCore import Qt
import importlib.util
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

# Ścieżka do pliku notes.py
ścieżka_notes = r'C:\Users\karol\OneDrive\Desktop\projekt\notes\notes.py'

# Załaduj moduł notes
notes_spec = importlib.util.spec_from_file_location('notes', ścieżka_notes)
notes_moduł = importlib.util.module_from_spec(notes_spec)
notes_spec.loader.exec_module(notes_moduł)

# Importuj klasę Note
Note = notes_moduł.Note
class NotesActiveMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.database = None
        self.notes_list = QComboBox()
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
        self.mainLabel.setText("Now you can choose your note, are you happy? 🐢 ")

        self.layout.addWidget(self.mainLabel)
        self.layout.addWidget(self.notes_list)

        self.load_archive_notes()

    def load_archive_notes(self):
        model = QStandardItemModel()

        model.setColumnCount(3)
        model.setHeaderData(0, Qt.Orientation.Horizontal, "Title 🦉")
        model.setHeaderData(1, Qt.Orientation.Horizontal, "Text 🐶")
        model.setHeaderData(2, Qt.Orientation.Horizontal, "Time 🦩")

        query = QSqlQuery()
        query.prepare("SELECT * FROM Notes WHERE active = 0")
        query.exec()

        while query.next():
            title = query.value(1)
            text = query.value(2)
            time = query.value(3)

            row = [QStandardItem(title), QStandardItem(text), QStandardItem(str(time))]
            model.appendRow(row)

        self.notes_list.setModel(model)

        delegate = QStyledItemDelegate()
        self.notes_list.setItemDelegate(delegate)

    def open_database(self):
        self.database = QSqlDatabase.addDatabase("QSQLITE")
        self.database.setDatabaseName('NotesDatabase.sqlite3')

        if not self.database.open():
            self.mainLabel.setText("Database is not open")
            return False
        self.load_archive_notes()
        return True
    
    def close_database(self):
        self.database.close()
