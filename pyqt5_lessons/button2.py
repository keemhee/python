from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QPushButton  # PyQt5 위젯들을 임포트
from PyQt5.QtCore import Qt  # QtCore 모듈에서 Qt 객체 임포트

class MainWindow(QMainWindow):  # QMainWindow를 상속받는 MainWindow 클래스 정의
    def __init__(self):
        super().__init__()  # 부모 클래스의 초기화 메서드 호출

        self.setWindowTitle("Button_2")  # 윈도우 제목 설정

        widget = QWidget()  # 중앙 위젯 생성
        h_layout = QHBoxLayout()  # 수평 레이아웃 생성

        widget.setLayout(h_layout)  # 중앙 위젯에 수평 레이아웃 설정
        self.setCentralWidget(widget)  # 중앙 위젯 설정

        button1 = QPushButton("버튼1")  # "버튼1" 텍스트를 가진 버튼 생성
        button1.setCheckable = True  # 버튼을 체크 가능하게 설정
        button1.clicked.connect(self.button_is_clicked)  # 버튼 클릭 시 호출될 함수 연결

        button2 = QPushButton("버튼2")  # "버튼2" 텍스트를 가진 버튼 생성
        button2.setCheckable = True  # 버튼을 체크 가능하게 설정
        button2.clicked.connect(self.button_is_clicked)  # 버튼 클릭 시 호출될 함수 연결

        h_layout.addWidget(button1)  # 수평 레이아웃에 첫 번째 버튼 추가
        h_layout.addWidget(button2)  # 수평 레이아웃에 두 번째 버튼 추가

        self.show()  # 윈도우 표시

    def button_is_clicked(self):  # 버튼 클릭 시 호출될 함수 정의
        print("CLICKED")  # 콘솔에 "CLICKED" 메시지 출력

app = QApplication([])  # QApplication 객체 생성
window = MainWindow()  # MainWindow 객체 생성
app.exec_()  # 이벤트 루프 실행