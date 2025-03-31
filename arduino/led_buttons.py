import serial  # 시리얼 통신을 위해 pyserial 라이브러리 임포트
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QApplication  # PyQt5를 사용하여 GUI 구성 요소 임포트

class ArduinoController(QWidget):  # QWidget을 상속받아 ArduinoController 클래스 정의
    def __init__(self):
        super().__init__()  # 부모 클래스의 생성자 호출
        self.setWindowTitle("LED CONTROLLER")  # 윈도우 제목 설정
        self.arduino = serial.Serial('COM3', 9600)  # Arduino와 시리얼 통신 설정 (포트: COM3, 보드레이트: 9600)

        widget = QWidget()  # 메인 위젯 생성
        b_layout = QHBoxLayout()  # 수평 레이아웃 생성

        b1 = QPushButton("ON")  # "ON" 버튼 생성
        b2 = QPushButton("OFF")  # "OFF" 버튼 생성

        b1.clicked.connect(self.clicked1)  # "ON" 버튼 클릭 시 clicked1 메서드 연결
        b2.clicked.connect(self.clicked2)  # "OFF" 버튼 클릭 시 clicked2 메서드 연결

        b_layout.addWidget(b1)  # 레이아웃에 "ON" 버튼 추가
        b_layout.addWidget(b2)  # 레이아웃에 "OFF" 버튼 추가

        widget.setLayout(b_layout)  # 메인 위젯에 레이아웃 설정
        self.setLayout(b_layout)  # 윈도우에 레이아웃 설정
        self.show()  # 윈도우 표시

    def clicked1(self):
        print("LED ON")  # 콘솔에 "LED ON" 출력
        self.arduino.write(b'1')  # Arduino로 '1' 전송 (LED 켜기 신호)

    def clicked2(self):
        print("LED OFF")  # 콘솔에 "LED OFF" 출력
        self.arduino.write(b'2')  # Arduino로 '2' 전송 (LED 끄기 신호)


if __name__ == '__main__':
    app = QApplication([])  # QApplication 객체 생성
    ex = ArduinoController()  # ArduinoController 객체 생성
    app.exec()  # 이벤트 루프 실행