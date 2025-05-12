"""
Script de teste para verificar a GUI.
"""
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Teste GUI")
    window.setGeometry(100, 100, 400, 300)
    
    # Widget central
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    
    # Layout
    layout = QVBoxLayout(central_widget)
    
    # Botão de teste
    button = QPushButton("Teste")
    layout.addWidget(button)
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 