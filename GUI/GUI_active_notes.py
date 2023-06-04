from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QTableView
from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSlot 
import importlib.util
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from GUI_note_box import Notes

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
        self.notes_window = None
        self.tableView = QTableView()
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
        self.layout.addWidget(self.tableView)

        self.load_active_notes()

        self.tableView.clicked.connect(self.handle_table_view_clicked)  # Dodanie sygnału clicked

    def load_active_notes(self):
        query = QSqlQuery()
        query.prepare("SELECT title, text, time FROM Notes WHERE active = 1")
        query.exec()

        data = []
        while query.next():
            column1 = query.value(0)
            column2 = query.value(1)
            column3 = query.value(2)
            data.append([column1, column2, column3])

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
        self.load_active_notes()

        return True
    
    @pyqtSlot(QModelIndex)
    def handle_table_view_clicked(self, index):
        selected_row = index.row()

        model = self.tableView.model()
        column_count = model.columnCount()

        selected_data = []
        for column in range(column_count):
            data = model.index(selected_row, column).data(Qt.ItemDataRole.DisplayRole)
            print(data)
            selected_data.append(data)
            
        note = Note("opened", selected_data[0], selected_data[1], selected_data[2], True)
        self.notes_window = Notes(selected_data[0], selected_data[1], selected_data[2], note)
        self.notes_window.show()
        
    
class NotesTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def rowCount(self, parent=QModelIndex()):
        return len(self.data)

    def columnCount(self, parent=QModelIndex()):
        return 3

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            row = index.row()
            col = index.column()
            value = self.data[row][col]
            return str(value)

        return None