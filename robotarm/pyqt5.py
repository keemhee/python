from PyQt5.QtCore import QTimer  # QTimer 클래스를 임포트
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel  # PyQt5 위젯들을 임포트
import serial  # 시리얼 통신을 위한 라이브러리 임포트

class ArduinoRead(QWidget):  # QWidget을 상속받는 ArduinoRead 클래스 정의
    def __init__(self):
        super().__init__()  # 부모 클래스의 초기화 메서드 호출
        self.setWindowTitle("Arduino")  # 윈도우 제목 설정
        self.serial = serial.Serial("COM3", 9600)  # 아두이노와 시리얼 통신 설정 (포트와 속도)
        self.timer = QTimer()  # 타이머 객체 생성
        self.timer.timeout.connect(self.read_data)  # 타이머가 만료될 때 호출될 함수 연결
        self.timer.start(1000)  # 타이머를 1초 간격으로 시작

        layout = QVBoxLayout()  # 수직 레이아웃 생성
        self.label = QLabel("ARDUINO DATA", self)  # 라벨 생성 및 초기 텍스트 설정
        layout.addWidget(self.label)  # 레이아웃에 라벨 추가
        self.setLayout(layout)  # 레이아웃을 현재 위젯의 레이아웃으로 설정

    def read_data(self):  # 시리얼 데이터를 읽어오는 함수 정의
        if self.serial.in_waiting > 0:  # 읽을 수 있는 데이터가 있는 경우
            data = self.serial.readline().decode('utf-8').rstrip()  # 한 줄의 데이터를 읽어서 디코딩 후 양 끝 공백 제거
            self.label.setText(f"DATA: {data}")  # 라벨의 텍스트를 읽어온 데이터로 업데이트

if __name__ == "__main__":  # 프로그램의 시작점
    app = QApplication([])  # QApplication 객체 생성
    window = ArduinoRead()  # ArduinoRead 객체 생성
    window.show()  # 윈도우 표시
    app.exec_()  # 이벤트 루프 실행