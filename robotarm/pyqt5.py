from PyQt5.QtCore import QTimer 
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
import serial

class ArduinoRead(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arduino")
        self.serial = serial.Serial("COM3", 9600)  # 아두이노와 연결
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_data) 
        self.timer.start(1000)  # 1초마다 데이터 읽기
        
        layout = QVBoxLayout()
        self.label = QLabel("ARDUINO DATA", self)
        layout.addWidget(self.label) 
        self.setLayout(layout)

    def read_data(self):
        if self.serial.in_waiting > 0:
            data = self.serial.readline().decode('utf-8').rstrip()
            self.label.setText(f"DATA: {data}")

if __name__ == "__main__":
    app = QApplication([])
    window = ArduinoRead()
    window.show()
    app.exec_()
