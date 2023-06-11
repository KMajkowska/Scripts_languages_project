from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QTableView, QHeaderView
from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSlot 
import importlib.util
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from GUI_note_box import Notes
from functions import CURRENT_NOTES_PATH
import datetime

# Ścieżka do pliku notes.py
ścieżka_notes = CURRENT_NOTES_PATH

# Załaduj moduł notes
notes_spec = importlib.util.spec_from_file_location('notes', ścieżka_notes)
notes_moduł = importlib.util.module_from_spec(notes_spec)
notes_spec.loader.exec_module(notes_moduł)

# Importuj klasę Note
Note = notes_moduł.Note
class NotesArchiveMainWindow(QMainWindow):
    def __init__(self, color, main):
        super().__init__()

        self.database = None
        self.notes_window = None
        self.tableView = QTableView()
        self.color = color
        self.main = main
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Open archive notes 🐬")
        self.setGeometry(100, 100, 300, 200)

        self.open_database()
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.mainLabel = QLabel()
        self.mainLabel.setText("Now you can choose your note, are you happy? \nJust click on the note, and it will open! 🐞")

        self.layout.addWidget(self.mainLabel)
        self.layout.addWidget(self.tableView)

        self.tableView.clicked.connect(self.handle_table_view_clicked)

        self.header = self.tableView.horizontalHeader()
        self.header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)


    def load_archive_notes(self):
        query = QSqlQuery()
        query.prepare("SELECT uid, title, text, time, last_edit, active FROM Notes WHERE active = 0")
        query.exec()

        data = []
        while query.next():
            self.uid = query.value(0)
            self.title = query.value(1)
            self.text = query.value(2)
            self.time = query.value(3)
            self.last_edit = query.value(4)
            self.active = query.value(5)
            self.reminder = query.value(6)
            data.append([self.title, self.text, self.time, self.last_edit])
        model = NotesTableModel(data)

        # Ustawianie modelu danych dla TableView
        self.tableView.setModel(model)
        self.tableView.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.tableView.setSelectionMode(QTableView.SelectionMode.NoSelection)
        self.tableView.horizontalHeader().setStretchLastSection(True)

    def open_database(self):
        self.database = QSqlDatabase.addDatabase("QSQLITE")
        self.database.setDatabaseName('NotesDatabase.sqlite3')
 
        if not self.database.open():
            self.mainLabel.setText("Database is not open")
            return False
        self.load_archive_notes()

        return True
    
    @pyqtSlot(QModelIndex)
    def handle_table_view_clicked(self, index):
        selected_row = index.row()

        self.model = self.tableView.model()
        column_count = self.model.columnCount()

        selected_data = []
        for column in range(column_count):
            data = self.model.index(selected_row, column).data()
            selected_data.append(data)
            
        note = Note(self.uid, selected_data[0], selected_data[1], selected_data[2], selected_data[3], self.active, datetime(2000, 1, 1, 0, 0))
        self.notes_window = Notes(selected_data[0], selected_data[1], selected_data[2], selected_data[3],note, self)
        self.notes_window.setStyleSheet(f"background-color: {self.color};")
        self.notes_window.show()
        
    def deleteNote(self):
        selected_row = self.tableView.currentIndex().row()

        if selected_row >= 0:
            self.model = self.tableView.model()
            self.model.removeRow(selected_row)

            self.tableView.setModel(self.model)
            self.model.layoutChanged.emit()
        else:
            print("No note selected.")

class NotesTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.columns = ["Title", "Note preview", "Creation date", "Last edit date"]

    def rowCount(self, parent=QModelIndex()):
        return len(self.data)

    def columnCount(self, parent=QModelIndex()):
        return 4

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            row = index.row()
            col = index.column()
            value = self.data[row][col]
            return str(value)

        return None
    
    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.columns[section]
            elif orientation == Qt.Orientation.Vertical:
                return f"{section + 1}"

        return super().headerData(section, orientation, role)
    
    def removeRow(self, row, parent=QModelIndex()):
        self.beginRemoveRows(parent, row, row)
        del self.data[row]
        self.endRemoveRows()
