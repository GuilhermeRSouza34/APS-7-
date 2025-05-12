"""
Script de teste para verificar a instalação do PyQt6.
"""
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Teste PyQt6")
    window.setGeometry(100, 100, 400, 200)
    
    label = QLabel("Se você está vendo esta janela, o PyQt6 está funcionando!", window)
    label.setGeometry(50, 50, 300, 100)
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 