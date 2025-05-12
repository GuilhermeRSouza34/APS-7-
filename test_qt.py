import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Teste PyQt6")
window.setGeometry(100, 100, 300, 100)

label = QLabel("Teste", window)
label.move(100, 40)

window.show()
sys.exit(app.exec()) 