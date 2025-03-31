from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow  # PyQt5 위젯들을 임포트

class MainWindow(QMainWindow):  # QMainWindow를 상속받는 MainWindow 클래스 정의
    def __init__(self):
        super().__init__()  # 부모 클래스의 초기화 메서드 호출
        self.button_is_checked = False  # 버튼의 체크 상태를 나타내는 변수 초기화

        self.setWindowTitle("Button01")  # 윈도우 제목 설정

        button = QPushButton("ON")  # "ON" 텍스트를 가진 버튼 생성
        button.setCheckable = True  # 버튼을 체크 가능하게 설정
        button.setObjectName("evilButton")  # 버튼의 객체 이름 설정
        button.clicked.connect(self.button_is_clicked)  # 버튼 클릭 시 호출될 함수 연결

        # 초기 스타일 시트 설정
        self.setStyleSheet("""
            QPushButton#evilButton {
                background-color: red;  # 배경색을 빨간색으로 설정
                border-style: outset;  # 테두리 스타일 설정
                border-width: 5px;  # 테두리 너비 설정
                border-color: beige;  # 테두리 색상 설정
                font-size: 20px;  # 글꼴 크기 설정
            }
        """)        

        self.setCentralWidget(button)  # 중앙 위젯으로 버튼 설정
        self.show()  # 윈도우 표시

    def button_is_clicked(self):  # 버튼 클릭 시 호출될 함수 정의
        self.button_is_checked = not self.button_is_checked  # 버튼의 체크 상태를 반전시킴
        if self.button_is_checked:
            #self.setStyleSheet("background-color: yellow")
            self.setStyleSheet("color: blue;"
                        "background-color: yellow;"
                        "selection-color: yellow;"
                        "selection-background-color: blue;")  # 스타일 시트 변경
            self.button.setText("OFF")  # 버튼 텍스트를 "OFF"로 변경
            print("LED ON")  # 콘솔에 "LED ON" 출력
        else:
            self.setStyleSheet("background-color: green")  # 배경색을 녹색으로 변경
            self.button.setText("ON")  # 버튼 텍스트를 "ON"으로 변경
            print("LED OFF")  # 콘솔에 "LED OFF" 출력

app = QApplication([])  # QApplication 객체 생성
window = MainWindow()  # MainWindow 객체 생성
app.exec_()  # 이벤트 루프 실행