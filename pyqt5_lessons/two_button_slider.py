from PyQt5.QtWidgets import QApplication, QSlider, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton  # PyQt5 위젯들을 임포트
from PyQt5.QtCore import Qt  # QtCore 모듈에서 Qt 객체 임포트

class MainWindow(QMainWindow):  # QMainWindow를 상속받는 MainWindow 클래스 정의
    def __init__(self):
        super().__init__()  # 부모 클래스의 초기화 메서드 호출

        self.setWindowTitle("2버튼 2슬라이더")  # 윈도우 제목 설정
        widget = QWidget()  # 중앙 위젯 생성
        h_layout = QHBoxLayout()  # 수평 레이아웃 생성
        v1_layout = QVBoxLayout()  # 첫 번째 수직 레이아웃 생성
        v2_layout = QVBoxLayout()  # 두 번째 수직 레이아웃 생성

        slider1 = QSlider(Qt.Horizontal)  # 첫 번째 슬라이더 생성 (수평)
        slider2 = QSlider(Qt.Horizontal)  # 두 번째 슬라이더 생성 (수평)

        b1 = QPushButton("b1")  # 첫 번째 버튼 생성
        b2 = QPushButton("b2")  # 두 번째 버튼 생성

        slider1.setMinimum(0)  # 첫 번째 슬라이더의 최소값 설정
        slider1.setMaximum(100)  # 첫 번째 슬라이더의 최대값 설정
        slider1.valueChanged.connect(self.slider_value_change_1)  # 첫 번째 슬라이더 값 변경 시 호출될 함수 연결
        slider2.setMinimum(0)  # 두 번째 슬라이더의 최소값 설정
        slider2.setMaximum(100)  # 두 번째 슬라이더의 최대값 설정
        slider2.valueChanged.connect(self.slider_value_change_2)  # 두 번째 슬라이더 값 변경 시 호출될 함수 연결

        b1.clicked.connect(self.click1)  # 첫 번째 버튼 클릭 시 호출될 함수 연결
        b2.clicked.connect(self.click2)  # 두 번째 버튼 클릭 시 호출될 함수 연결

        # 레이아웃에 위젯 추가
        v1_layout.addWidget(b1)  # 첫 번째 수직 레이아웃에 첫 번째 버튼 추가
        v1_layout.addWidget(b2)  # 첫 번째 수직 레이아웃에 두 번째 버튼 추가
        v2_layout.addWidget(slider1)  # 두 번째 수직 레이아웃에 첫 번째 슬라이더 추가
        v2_layout.addWidget(slider2)  # 두 번째 수직 레이아웃에 두 번째 슬라이더 추가

        h_layout.addLayout(v1_layout)  # 수평 레이아웃에 첫 번째 수직 레이아웃 추가
        h_layout.addLayout(v2_layout)  # 수평 레이아웃에 두 번째 수직 레이아웃 추가
        self.setCentralWidget(widget)  # 중앙 위젯 설정
        widget.setLayout(h_layout)  # 중앙 위젯에 수평 레이아웃 설정
        self.show()  # 윈도우 표시

    def click1(self):  # 첫 번째 버튼 클릭 시 호출될 함수 정의
        print("b1 clicked")  # 콘솔에 메시지 출력

    def click2(self):  # 두 번째 버튼 클릭 시 호출될 함수 정의
        print("b2 clicked")  # 콘솔에 메시지 출력

    def slider_value_change_1(self, value):  # 첫 번째 슬라이더 값 변경 시 호출될 함수 정의
        print(value)  # 현재 슬라이더 값을 콘솔에 출력
    
    def slider_value_change_2(self, value):  # 두 번째 슬라이더 값 변경 시 호출될 함수 정의
        print(value)  # 현재 슬라이더 값을 콘솔에 출력

app = QApplication([])  # QApplication 객체 생성
window = MainWindow()  # MainWindow 객체 생성
app.exec_()  # 이벤트 루프 실행