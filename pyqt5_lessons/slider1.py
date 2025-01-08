from PyQt5.QtWidgets import QApplication, QMainWindow,  QWidget, QVBoxLayout, QSlider

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Slider")

        widget = QWidget()
        v_layout = QVBoxLayout()

        slider = QSlider()   #default가 vertical로 움직이는 거
        slider.setMinimum(0)
        slider.setMaximum(100)
        slider.setSingleStep(5) #없으면 1. 얼마나 옮길래  키보드로 실행
        slider.valueChanged.connect(self.slider_value_changed)

        v_layout.addWidget(slider)
        widget.setLayout(v_layout)

        self.setCentralWidget(widget)
        self.show()

    def slider_value_changed(self,value):
        print(value)         #바 움직이면 값 움직이는 거 나옴

app = QApplication([])
window = MainWindow()

app.exec_()