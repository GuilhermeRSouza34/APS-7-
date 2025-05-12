"""
Interface gráfica principal do sistema SCALE.
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QLabel, QFileDialog, QTableWidget,
                            QTableWidgetItem, QMessageBox, QTabWidget,
                            QGroupBox, QFormLayout, QLineEdit, QSpinBox,
                            QDoubleSpinBox, QComboBox)
from PyQt6.QtCore import Qt
import pandas as pd
from typing import Optional, Dict
import os
from datetime import datetime

from ..core.lci_manager import LCIManager
from ..core.emergy_calculator import EmergyCalculator, EmergyResult

class MainWindow(QMainWindow):
    """Janela principal da aplicação."""
    
    def __init__(self):
        """Inicializa a janela principal."""
        super().__init__()
        self.setWindowTitle("SCALE - Sistema de Cálculo Emergético")
        self.setMinimumSize(1000, 800)
        
        # Inicializa os componentes do sistema
        self.lci_manager = LCIManager()
        self.emergy_calculator = EmergyCalculator()
        
        # Configura a interface
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura os elementos da interface."""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout(central_widget)
        
        # Criar abas
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)
        
        # Aba de Importação
        import_tab = QWidget()
        self._setup_import_tab(import_tab)
        tab_widget.addTab(import_tab, "Importação")
        
        # Aba de Cálculos
        calc_tab = QWidget()
        self._setup_calc_tab(calc_tab)
        tab_widget.addTab(calc_tab, "Cálculos")
        
        # Aba de Resultados
        results_tab = QWidget()
        self._setup_results_tab(results_tab)
        tab_widget.addTab(results_tab, "Resultados")
    
    def _setup_import_tab(self, tab: QWidget):
        """Configura a aba de importação."""
        layout = QVBoxLayout(tab)
        
        # Grupo de importação
        import_group = QGroupBox("Importar Dados LCI")
        import_layout = QVBoxLayout()
        
        # Botões de importação
        btn_layout = QHBoxLayout()
        self.import_btn = QPushButton("Importar LCI")
        self.import_btn.clicked.connect(self._import_lci)
        btn_layout.addWidget(self.import_btn)
        
        self.export_btn = QPushButton("Exportar LCI")
        self.export_btn.clicked.connect(self._export_lci)
        btn_layout.addWidget(self.export_btn)
        
        import_layout.addLayout(btn_layout)
        import_group.setLayout(import_layout)
        layout.addWidget(import_group)
        
        # Tabela de visualização
        self.table = QTableWidget()
        layout.addWidget(self.table)
        
        # Informações da matriz
        info_group = QGroupBox("Informações da Matriz")
        info_layout = QFormLayout()
        self.matrix_info = QLabel("Nenhuma matriz carregada")
        info_layout.addRow("Status:", self.matrix_info)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
    
    def _setup_calc_tab(self, tab: QWidget):
        """Configura a aba de cálculos."""
        layout = QVBoxLayout(tab)
        
        # Grupo de configuração
        config_group = QGroupBox("Configuração dos Cálculos")
        config_layout = QFormLayout()
        
        # Seleção de matriz
        self.matrix_combo = QComboBox()
        self.matrix_combo.currentTextChanged.connect(self._update_transformity)
        config_layout.addRow("Matriz LCI:", self.matrix_combo)
        
        # Fatores de transformidade
        self.transformity_inputs = {}
        for factor in ['Energia Solar', 'Energia Eólica', 'Água', 'Matéria Prima']:
            spin = QDoubleSpinBox()
            spin.setRange(0, 1000000)
            spin.setValue(1.0)
            spin.setDecimals(2)
            self.transformity_inputs[factor] = spin
            config_layout.addRow(f"{factor}:", spin)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Botão de cálculo
        self.calc_btn = QPushButton("Calcular Emergia")
        self.calc_btn.clicked.connect(self._calculate_emergy)
        layout.addWidget(self.calc_btn)
    
    def _setup_results_tab(self, tab: QWidget):
        """Configura a aba de resultados."""
        layout = QVBoxLayout(tab)
        
        # Tabela de resultados
        self.results_table = QTableWidget()
        layout.addWidget(self.results_table)
        
        # Informações dos resultados
        info_group = QGroupBox("Informações dos Resultados")
        info_layout = QFormLayout()
        self.results_info = QLabel("Nenhum cálculo realizado")
        info_layout.addRow("Status:", self.results_info)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Botões de exportação
        btn_layout = QHBoxLayout()
        self.export_results_btn = QPushButton("Exportar Resultados")
        self.export_results_btn.clicked.connect(self._export_results)
        btn_layout.addWidget(self.export_results_btn)
        layout.addLayout(btn_layout)
    
    def _import_lci(self):
        """Importa um arquivo LCI."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar arquivo LCI",
            "",
            "Arquivos CSV (*.csv);;Arquivos Excel (*.xlsx *.xls)"
        )
        
        if file_path:
            name = os.path.splitext(os.path.basename(file_path))[0]
            success = self.lci_manager.import_lci_file(file_path, name)
            if success:
                self._display_matrix(self.lci_manager.get_matrix(name))
                self._update_matrix_info(name)
                self._update_matrix_combo()
            else:
                QMessageBox.critical(self, "Erro", "Falha ao importar arquivo")
    
    def _export_lci(self):
        """Exporta a matriz LCI atual."""
        if not self.lci_manager.get_matrix():
            QMessageBox.warning(self, "Aviso", "Nenhuma matriz para exportar")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar matriz LCI",
            "",
            "Arquivos CSV (*.csv);;Arquivos Excel (*.xlsx)"
        )
        
        if file_path:
            name = self.matrix_combo.currentText()
            success = self.lci_manager.export_matrix(name, file_path)
            if not success:
                QMessageBox.critical(self, "Erro", "Falha ao exportar arquivo")
    
    def _display_matrix(self, matrix: Optional[pd.DataFrame]):
        """Exibe a matriz LCI na tabela."""
        if matrix is None:
            return
        
        self.table.setRowCount(len(matrix))
        self.table.setColumnCount(len(matrix.columns))
        self.table.setHorizontalHeaderLabels(matrix.columns)
        
        for i in range(len(matrix)):
            for j in range(len(matrix.columns)):
                value = str(matrix.iloc[i, j])
                self.table.setItem(i, j, QTableWidgetItem(value))
    
    def _update_matrix_info(self, name: str):
        """Atualiza as informações da matriz."""
        metadata = self.lci_manager.get_matrix_metadata(name)
        if metadata:
            info = (f"Matriz: {name}\n"
                   f"Arquivo: {metadata['file_path']}\n"
                   f"Importado em: {metadata['import_date']}\n"
                   f"Linhas: {metadata['rows']}, Colunas: {metadata['columns']}")
            self.matrix_info.setText(info)
    
    def _update_matrix_combo(self):
        """Atualiza o combo box de seleção de matriz."""
        self.matrix_combo.clear()
        self.matrix_combo.addItems(self.lci_manager.list_available_matrices())
    
    def _update_transformity(self):
        """Atualiza os campos de transformidade com base na matriz selecionada."""
        name = self.matrix_combo.currentText()
        if not name:
            return
        
        matrix = self.lci_manager.get_matrix(name)
        if matrix is None:
            return
        
        # Atualiza os valores dos campos de transformidade
        for factor, spin in self.transformity_inputs.items():
            if factor in matrix.columns:
                spin.setEnabled(True)
            else:
                spin.setEnabled(False)
    
    def _calculate_emergy(self):
        """Realiza os cálculos emergéticos."""
        name = self.matrix_combo.currentText()
        if not name:
            QMessageBox.warning(self, "Aviso", "Selecione uma matriz LCI")
            return
        
        matrix = self.lci_manager.get_matrix(name)
        if matrix is None:
            return
        
        # Coleta os fatores de transformidade
        transformity_factors = {
            factor: spin.value()
            for factor, spin in self.transformity_inputs.items()
            if spin.isEnabled()
        }
        
        # Configura e realiza o cálculo
        self.emergy_calculator.set_transformity_factors(transformity_factors)
        result = self.emergy_calculator.calculate_emergy(matrix)
        
        # Exibe os resultados
        self._display_results(result)
    
    def _display_results(self, result: EmergyResult):
        """Exibe os resultados do cálculo."""
        # Atualiza a tabela de resultados
        self.results_table.setRowCount(len(result.process_emergy))
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(['Processo', 'Emergia'])
        
        for i, (process, emergy) in enumerate(result.process_emergy.items()):
            self.results_table.setItem(i, 0, QTableWidgetItem(process))
            self.results_table.setItem(i, 1, QTableWidgetItem(f"{emergy:.2f}"))
        
        # Atualiza as informações
        info = (f"Total Emergia: {result.total_emergy:.2f}\n"
                f"Data Cálculo: {result.calculation_date}\n"
                f"Processos: {result.metadata['process_count']}")
        self.results_info.setText(info)
    
    def _export_results(self):
        """Exporta os resultados do cálculo."""
        result = self.emergy_calculator.get_results('latest')
        if not result:
            QMessageBox.warning(self, "Aviso", "Nenhum resultado para exportar")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar resultados",
            "",
            "Arquivos CSV (*.csv);;Arquivos Excel (*.xlsx)"
        )
        
        if file_path:
            success = self.emergy_calculator.export_results(result['latest'], file_path)
            if not success:
                QMessageBox.critical(self, "Erro", "Falha ao exportar resultados") 