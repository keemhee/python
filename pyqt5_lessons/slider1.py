from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QSlider  # PyQt5 위젯들을 임포트

class MainWindow(QMainWindow):  # QMainWindow를 상속받는 MainWindow 클래스 정의
    def __init__(self):
        super().__init__()  # 부모 클래스의 초기화 메서드 호출

        self.setWindowTitle("Slider")  # 윈도우 제목 설정

        widget = QWidget()  # 중앙 위젯 생성
        v_layout = QVBoxLayout()  # 수직 레이아웃 생성

        slider = QSlider()  # 슬라이더 생성 (기본값은 수직)
        slider.setMinimum(0)  # 슬라이더의 최소값 설정
        slider.setMaximum(100)  # 슬라이더의 최대값 설정
        slider.setSingleStep(5)  # 슬라이더의 단일 스텝 설정 (없으면 기본값 1)
        slider.valueChanged.connect(self.slider_value_changed)  # 슬라이더 값 변경 시 호출될 함수 연결

        v_layout.addWidget(slider)  # 수직 레이아웃에 슬라이더 추가
        widget.setLayout(v_layout)  # 중앙 위젯에 수직 레이아웃 설정

        self.setCentralWidget(widget)  # 중앙 위젯 설정
        self.show()  # 윈도우 표시

    def slider_value_changed(self, value):  # 슬라이더 값 변경 시 호출될 함수 정의
        print(value)  # 현재 슬라이더 값을 콘솔에 출력

app = QApplication([])  # QApplication 객체 생성
window = MainWindow()  # MainWindow 객체 생성

app.exec_()  # 이벤트 루프 실행