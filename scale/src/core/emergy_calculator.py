"""
Módulo para cálculos emergéticos baseados em álgebra emergética.
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class EmergyResult:
    """Classe para armazenar resultados dos cálculos emergéticos."""
    total_emergy: float
    process_emergy: Dict[str, float]
    transformity: Dict[str, float]
    calculation_date: datetime
    metadata: Dict

class EmergyCalculator:
    """Classe responsável pelos cálculos emergéticos."""
    
    def __init__(self):
        """Inicializa a calculadora de emergia."""
        self._transformity_factors: Dict[str, float] = {}
        self._results: Dict[str, EmergyResult] = {}
        self._default_transformity = {
            'Energia Solar': 1.0,
            'Energia Eólica': 1500.0,
            'Água': 41000.0,
            'Matéria Prima': 100000.0
        }
    
    def set_transformity_factors(self, factors: Dict[str, float]) -> None:
        """
        Define os fatores de transformidade para os cálculos.
        
        Args:
            factors: Dicionário com os fatores de transformidade
        """
        self._transformity_factors = {**self._default_transformity, **factors}
    
    def calculate_emergy(self, lci_matrix: pd.DataFrame) -> EmergyResult:
        """
        Calcula a emergia total do sistema.
        
        Args:
            lci_matrix: Matriz LCI com os dados de entrada
            
        Returns:
            EmergyResult com os resultados dos cálculos
        """
        # Converter a matriz para numpy array
        matrix = lci_matrix.values
        process_names = lci_matrix['Processo'].values
        
        # Aplicar fatores de transformidade
        transformity_array = np.array([self._transformity_factors.get(col, 1.0) 
                                     for col in lci_matrix.columns if col != 'Processo'])
        
        # Calcular emergia (multiplicação elemento a elemento)
        emergy = matrix[:, 1:] * transformity_array
        
        # Calcular emergia por processo
        process_emergy = {}
        for i, process in enumerate(process_names):
            process_emergy[process] = float(np.sum(emergy[i]))
        
        # Calcular emergia total
        total_emergy = float(np.sum(emergy))
        
        # Criar resultado
        result = EmergyResult(
            total_emergy=total_emergy,
            process_emergy=process_emergy,
            transformity=self._transformity_factors.copy(),
            calculation_date=datetime.now(),
            metadata={
                'matrix_shape': lci_matrix.shape,
                'process_count': len(process_names)
            }
        )
        
        self._results['latest'] = result
        return result
    
    def calculate_network_emergy(self, 
                               input_matrix: pd.DataFrame,
                               process_matrix: pd.DataFrame) -> Tuple[EmergyResult, EmergyResult]:
        """
        Calcula a emergia em uma rede de processos.
        
        Args:
            input_matrix: Matriz de entradas
            process_matrix: Matriz de processos
            
        Returns:
            Tuple com EmergyResult para entradas e processos
        """
        input_result = self.calculate_emergy(input_matrix)
        process_result = self.calculate_emergy(process_matrix)
        
        self._results['input'] = input_result
        self._results['process'] = process_result
        
        return input_result, process_result
    
    def get_results(self, result_type: Optional[str] = None) -> Dict[str, EmergyResult]:
        """
        Retorna os resultados dos cálculos.
        
        Args:
            result_type: Tipo específico de resultado desejado
            
        Returns:
            Dicionário com os resultados
        """
        if result_type:
            return {result_type: self._results.get(result_type)}
        return self._results
    
    def export_results(self, result: EmergyResult, file_path: str) -> bool:
        """
        Exporta os resultados para um arquivo.
        
        Args:
            result: Resultado a ser exportado
            file_path: Caminho do arquivo de saída
            
        Returns:
            bool: True se a exportação foi bem-sucedida
        """
        try:
            # Criar DataFrame com os resultados
            data = {
                'Processo': list(result.process_emergy.keys()),
                'Emergia': list(result.process_emergy.values())
            }
            df = pd.DataFrame(data)
            
            # Adicionar metadados
            metadata = pd.DataFrame([{
                'Total Emergia': result.total_emergy,
                'Data Cálculo': result.calculation_date,
                'Número de Processos': result.metadata['process_count']
            }])
            
            # Exportar
            if file_path.endswith('.csv'):
                df.to_csv(file_path, index=False)
                metadata.to_csv(file_path.replace('.csv', '_metadata.csv'), index=False)
            elif file_path.endswith('.xlsx'):
                with pd.ExcelWriter(file_path) as writer:
                    df.to_excel(writer, sheet_name='Resultados', index=False)
                    metadata.to_excel(writer, sheet_name='Metadados', index=False)
            else:
                raise ValueError("Formato de arquivo não suportado")
            
            return True
        except Exception as e:
            print(f"Erro ao exportar resultados: {str(e)}")
            return False 