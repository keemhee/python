import serial
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QApplication

class ArduinoController(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LED CONTROLLER")
        self.arduino = serial.Serial('COM3', 9600)

        widget = QWidget()
        b_layout = QHBoxLayout()

        b1 = QPushButton("ON")
        b2 = QPushButton("OFF")

        b1.clicked.connect(self.clicked1)
        b2.clicked.connect(self.clicked2)

        b_layout.addWidget(b1)
        b_layout.addWidget(b2)

        widget.setLayout(b_layout)
        self.setLayout(b_layout)
        self.show()

    def clicked1(self):
        print("LED ON")
        self.arduino.write(b'1')
        
    def clicked2(self):
        print("LED OFF")
        self.arduino.write(b'2')



if __name__ == '__main__':
    app = QApplication([])
    ex = ArduinoController()
    app.exec()