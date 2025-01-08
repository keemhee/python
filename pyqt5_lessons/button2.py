from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout,QPushButton
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Button_2") 

        widget = QWidget()
        h_layout = QHBoxLayout()

        widget.setLayout(h_layout)
        self.setCentralWidget(widget)

        button1 = QPushButton("버튼1")
        button1.setCheckable = True
        button1.clicked.connect(self.button_is_clicked)

        button2 = QPushButton("버튼2")
        button2.setCheckable = True
        button2.clicked.connect(self.button_is_clicked)

       
        self.show()

    def button_is_clicked(self):
        print("CLICKED")

app = QApplication([])
window = MainWindow()
app.exec_()