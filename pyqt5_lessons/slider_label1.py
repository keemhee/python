from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QSlider, QLineEdit, QLabel  # PyQt5 위젯들을 임포트
from PyQt5.QtCore import Qt  # QtCore 모듈에서 Qt 객체 임포트

class MainWindow(QMainWindow):  # QMainWindow를 상속받는 MainWindow 클래스 정의
    def __init__(self):
        super().__init__()  # 부모 클래스의 초기화 메서드 호출

        self.setWindowTitle("Slider")  # 윈도우 제목 설정

        widget = QWidget()  # 중앙 위젯 생성
        h_layout = QHBoxLayout()  # 수평 레이아웃 생성
        label = QLabel()  # 레이블 생성
        value = QLineEdit()  # 텍스트 입력 위젯 생성
        slider = QSlider(Qt.Horizontal)  # 수평 슬라이더 생성 (기본값은 수직)

        slider.setMinimum(0)  # 슬라이더의 최소값 설정
        slider.setMaximum(100)  # 슬라이더의 최대값 설정
        # slider.setSingleStep(5)  # 슬라이더의 단일 스텝 설정 (없으면 기본값 1)

        slider.valueChanged.connect(self.slider_value_changed)  # 슬라이더 값 변경 시 호출될 함수 연결
        value.textChanged.connect(label.setText)  # 텍스트 입력 변경 시 레이블 텍스트 변경

        h_layout.addWidget(slider)  # 수평 레이아웃에 슬라이더 추가
        h_layout.addWidget(label)  # 수평 레이아웃에 레이블 추가
        widget.setLayout(h_layout)  # 중앙 위젯에 수평 레이아웃 설정

        self.setCentralWidget(widget)  # 중앙 위젯 설정
        self.show()  # 윈도우 표시

    def slider_value_changed(self, value):  # 슬라이더 값 변경 시 호출될 함수 정의
        print(value)  # 현재 슬라이더 값을 콘솔에 출력

app = QApplication([])  # QApplication 객체 생성
window = MainWindow()  # MainWindow 객체 생성

app.exec_()  # 이벤트 루프 실행