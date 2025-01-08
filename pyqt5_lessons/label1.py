from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Label")
        widget = QWidget()
        v_layout = QVBoxLayout()
        #input = QLineEdit()
        label = QLabel()

        #input.textChanged.connect(label.setText)
        label.setText("abcd")

        #v_layout.addWidget(input)
        v_layout.addWidget(label)
        widget.setLayout(v_layout)
        self.setCentralWidget(widget)
        self.show()


app = QApplication([])
window = MainWindow()
app.exec_()