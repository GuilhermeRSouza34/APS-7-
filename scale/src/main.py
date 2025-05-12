"""
Arquivo principal do sistema SCALE.
"""
import sys
import os

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from src.gui.main_window import MainWindow

def main():
    """Função principal que inicia a aplicação."""
    print("Iniciando aplicação...")
    app = QApplication(sys.argv)
    print("Criando janela principal...")
    window = MainWindow()
    print("Mostrando janela...")
    window.show()
    print("Iniciando loop de eventos...")
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 