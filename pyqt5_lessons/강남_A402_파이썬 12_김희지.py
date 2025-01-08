from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QHBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("b1b2")
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QHBoxLayout(widget)

        self.b1_is_checked = False
        self.b2_is_checked = False 

        self.b1 = QPushButton("b1")
        self.b1.setCheckable(True)
        self.b1.clicked.connect(self.clicked1)
        layout.addWidget(self.b1)

        self.b2 = QPushButton("b2")
        self.b2.setCheckable(True)
        self.b2.clicked.connect(self.clicked2)
        layout.addWidget(self.b2)

        self.show()

    def clicked1(self):
        self.b1_is_checked = not self.b1_is_checked
        if self.b1.isChecked():
            self.b1.setStyleSheet("color: blue;" 
                               "background-color: yellow;")
        else:
            self.setStyleSheet("")
        print("b1 clicked")

    def clicked2(self):
        self.b2_is_checked = not self.b2_is_checked
        if self.b2.isChecked():
            self.b2.setStyleSheet("color: red;"
                               "background-color: green")
        else:
            self.setStyleSheet("")
        print("b2 clicked")

app = QApplication([])
window = MainWindow()
app.exec_()