from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Button01")

        button = QPushButton("누름")
        button.setCheckable = True
        button.clicked.connect(self.button_is_clicked)

        self.setCentralWidget(button)
        self.show()

    def button_is_clicked(self):
        print("CLICKED!!!")

app = QApplication([])
window = MainWindow()

app.exec_()