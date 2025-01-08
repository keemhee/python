from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.button_is_checked = False

        self.setWindowTitle("Button01")

        button = QPushButton("ON")
        button.setCheckable = True
        button.setObjectName("evilButton")
        button.clicked.connect(self.button_is_clicked)
        button.setText

 # 초기 스타일 시트 설정

        self.setStyleSheet("""
            QPushButton#evilButton {
                background-color: red;
                border-style: outset;
                border-width: 5px;
                border-color: beige;
                font-size: 20px;
            }
        """)        

        self.setCentralWidget(button)
        self.show()

    def button_is_clicked(self):
        self.button_is_checked = not self.button_is_checked       #앞의 상태와 뒤의 상태가 반대가 됨. 한 번 누르면 fasle->true 또 누르면 true->false
        if self.button_is_checked:
            #self.setStyleSheet("background-color: yellow")
            self.setStyleSheet("color: blue;"
                        "background-color: yellow;"
                        "selection-color: yellow;"
                        "selection-background-color: blue;")
            self.button.setText("OFF")                            #켜졌으니 off만들기 위해선 눌러라라는 의미?
            print("LED ON")
        else:
            self.setStyleSheet("background-color: green")          #초기상태. 투명?하양?
            self.button.setText("ON")
            print("LED OFF")
        

app = QApplication([])
window = MainWindow()
app.exec_()
