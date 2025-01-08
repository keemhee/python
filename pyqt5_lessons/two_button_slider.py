from PyQt5.QtWidgets import QApplication, QSlider, QWidget, QMainWindow,  QVBoxLayout, QHBoxLayout, QPushButton #QLineEdit, QLabel
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("2버튼 2슬라이더")
        widget = QWidget()
        h_layout = QHBoxLayout()
        v1_layout = QVBoxLayout()
        v2_layout = QVBoxLayout()
        #label1 = QLabel()
        #label2 = QLabel()
        #input1 = QLineEdit()
        #input2 = QLineEdit()

        slider1 = QSlider(Qt.Horizontal) 
        slider2 = QSlider(Qt.Horizontal)

        b1 = QPushButton("b1")
        b2 = QPushButton("b2")

        slider1.setMinimum(0)
        slider1.setMaximum(100)
        slider1.valueChanged.connect(self.slider_value_change_1)
        slider2.setMinimum(0)
        slider2.setMaximum(100)
        slider2.valueChanged.connect(self.slider_value_change_2)

        b1.clicked.connect(self.click1)
        b2.clicked.connect(self.click2)


#뭐가 뭐를 품는지 잘 확인해서 추가해주기
#위젯은 하나하나
#레이아웃은 구역

        v1_layout.addWidget(b1)
        v1_layout.addWidget(b2)
        v2_layout.addWidget(slider1)
        v2_layout.addWidget(slider2)
        #v2_layout.addWidget(label1)
        #v2_layout.addWidget(label2)



        h_layout.addLayout(v1_layout)
        h_layout.addLayout(v2_layout)
        self.setCentralWidget(widget)
        widget.setLayout(h_layout)
        self.show()

    def click1(self):
        print("b1 clicked")

    def click2(self):
        print("b2 clicked")

    def slider_value_change_1(self,value):
        print(value)
    
    def slider_value_change_2(self,value):
        print(value)

app = QApplication([])
window = MainWindow()
app.exec_()