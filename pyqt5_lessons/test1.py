from PyQt5.QtWidgets import QApplication, QWidget

app = QApplication([])

window = QWidget()
window.setWindowTitle("My First PyQt5")

window.show()

app.exec_()