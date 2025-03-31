from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton  # PyQt5 위젯들을 임포트

class MainWindow(QMainWindow):  # QMainWindow를 상속받는 MainWindow 클래스 정의
    def __init__(self):
        super().__init__()  # 부모 클래스의 초기화 메서드 호출

        self.setWindowTitle("Button01")  # 윈도우 제목 설정

        button = QPushButton("누름")  # "누름" 텍스트를 가진 버튼 생성
        button.setCheckable = True  # 버튼을 체크 가능하게 설정
        button.clicked.connect(self.button_is_clicked)  # 버튼 클릭 시 호출될 함수 연결

        self.setCentralWidget(button)  # 중앙 위젯으로 버튼 설정
        self.show()  # 윈도우 표시

    def button_is_clicked(self):  # 버튼 클릭 시 호출될 함수 정의
        print("CLICKED!!!")  # 콘솔에 "CLICKED!!!" 메시지 출력

app = QApplication([])  # QApplication 객체 생성
window = MainWindow()  # MainWindow 객체 생성

app.exec_()  # 이벤트 루프 실행