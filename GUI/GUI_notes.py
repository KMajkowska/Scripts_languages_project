from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QListWidget, QHBoxLayout, QPushButton, QDateTimeEdit, QLabel, QLineEdit, QFileDialog, QListWidgetItem
import sys

class NotesMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notateczki")
        self.setMinimumSize(300,300)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.label = QLabel()
        self.label.setText("test")

        self.layout.addWidget(self.label)

def main():
    app = QApplication(sys.argv)
    window = NotesMainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()