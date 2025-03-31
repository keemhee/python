from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel  # PyQt5 위젯들을 임포트

class MainWindow(QMainWindow):  # QMainWindow를 상속받는 MainWindow 클래스 정의
    def __init__(self):
        super().__init__()  # 부모 클래스의 초기화 메서드 호출

        self.setWindowTitle("Label")  # 윈도우 제목 설정
        widget = QWidget()  # 중앙 위젯 생성
        v_layout = QVBoxLayout()  # 수직 레이아웃 생성

        # input = QLineEdit()  # 텍스트 입력 위젯 생성 (주석 처리됨)
        label = QLabel()  # 라벨 생성

        # input.textChanged.connect(label.setText)  # 텍스트 입력 변경 시 라벨 텍스트 변경 (주석 처리됨)
        label.setText("abcd")  # 라벨 텍스트를 "abcd"로 설정

        # v_layout.addWidget(input)  # 수직 레이아웃에 텍스트 입력 위젯 추가 (주석 처리됨)
        v_layout.addWidget(label)  # 수직 레이아웃에 라벨 추가
        widget.setLayout(v_layout)  # 중앙 위젯에 수직 레이아웃 설정
        self.setCentralWidget(widget)  # 중앙 위젯 설정
        self.show()  # 윈도우 표시

app = QApplication([])  # QApplication 객체 생성
window = MainWindow()  # MainWindow 객체 생성
app.exec_()  # 이벤트 루프 실행