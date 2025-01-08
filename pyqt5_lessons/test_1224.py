import serial
import threading
import time
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout

class JDamr(object):
    def __init__(self, com="COM4"):
        self.ser = serial.Serial(com, 115200)
        if self.ser.isOpen():
            print("JDamr serial port opened!")
        else:
            print("Can't open JDamr serial port!")
        time.sleep(1)
        self.callback = None  # PyQt에서 값을 업데이트하기 위한 콜백 함수

    def send_command(self, command):
        """STM32로 명령 전송"""
        try:
            self.ser.write(command)
            print(f"Sent command: {command}")
        except Exception as e:
            print(f"Error sending command: {e}")

    def receive_data(self):
        self.ser.flushInput()

        while True:
            head = bytearray(self.ser.read())[0]
            if head == 0xf5:
                payload = []
                length = bytearray(self.ser.read())[0]
                for i in range(length):
                    value = bytearray(self.ser.read())[0]
                    payload.append(value)
                self.parse_cmd(payload)

    def receive_thread(self):
        try:
            task_name = "serial_thread"
            rx_task = threading.Thread(target=self.receive_data, name=task_name)
            rx_task.setDaemon(True)
            rx_task.start()
            print("Start serial receive thread")
            time.sleep(0.05)
        except Exception as e:
            print(f"Error starting thread: {e}")

    

    def parse_cmd(self, payload):
        print(payload)
        encode1 = int.from_bytes(payload, byteorder="big")
        print(encode1)
        if self.callback:  # 콜백 함수가 설정되었을 때 값을 전달
            self.callback(encode1)


class MainWindow(QMainWindow):
    def __init__(self, bot):
        super().__init__()

        self.bot = bot
        self.bot.callback = self.update_label  # JDamr 객체와 연결
        self.setWindowTitle("Serial Data Viewer")

        # PyQt 위젯 설정
        widget = QWidget()
        v_layout = QVBoxLayout()

        # 데이터 표시용 Label
        self.label = QLabel()
        self.label.setText("Waiting for data...")
        v_layout.addWidget(self.label)

        # 버튼 추가
        h_layout = QHBoxLayout()
        self.on_button = QPushButton("Turn LED ON")
        self.off_button = QPushButton("Turn LED OFF")
        h_layout.addWidget(self.on_button)
        h_layout.addWidget(self.off_button)

        # 버튼 클릭 이벤트 연결
        self.on_button.clicked.connect(self.turn_led_on)
        self.off_button.clicked.connect(self.turn_led_off)

        v_layout.addLayout(h_layout)
        widget.setLayout(v_layout)
        self.setCentralWidget(widget)

    def update_label(self, value):
        """Label 업데이트 함수"""
        self.label.setText(f"Received: {value}")

    def turn_led_on(self):
        """LED 켜기 명령 전송"""
        self.bot.send_command(b'\xF5\x01\x01')  # ON 명령

    def turn_led_off(self):
        """LED 끄기 명령 전송"""
        self.bot.send_command(b'\xF5\x01\x00')  # OFF 명령


if __name__ == '__main__':
    import sys

    # JDamr 객체 생성
    com = 'COM5'
    bot = JDamr(com)
    time.sleep(1)
    bot.receive_thread()

    # PyQt5 GUI 실행
    app = QApplication(sys.argv)
    window = MainWindow(bot)
    window.show()
    sys.exit(app.exec_())
