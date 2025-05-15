"""
Módulo para gerenciamento de dados de Inventário do Ciclo de Vida (LCI).
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import os

class LCIManager:
    """Classe responsável pelo gerenciamento de dados LCI."""
    
    def __init__(self):
        """Inicializa o gerenciador de LCI."""
        self._data: Dict[str, pd.DataFrame] = {}
        self._current_matrix: Optional[pd.DataFrame] = None
        self._metadata: Dict[str, Dict] = {}
    
    def import_lci_file(self, file_path: str, name: str) -> bool:
        """
        Importa um arquivo LCI (CSV ou Excel).
        
        Args:
            file_path: Caminho do arquivo
            name: Nome para identificar o conjunto de dados
            
        Returns:
            bool: True se a importação foi bem-sucedida
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
            
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.txt'):
                # Tenta ler como CSV, se der erro tenta como tabulado
                try:
                    df = pd.read_csv(file_path)
                except Exception:
                    df = pd.read_csv(file_path, sep='\t')
            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            else:
                raise ValueError("Formato de arquivo não suportado")
            
            if not self.validate_matrix(df):
                raise ValueError("Matriz LCI inválida")
            
            self._data[name] = df
            self._current_matrix = df
            self._metadata[name] = {
                'file_path': file_path,
                'import_date': pd.Timestamp.now(),
                'rows': len(df),
                'columns': len(df.columns)
            }
            return True
        except Exception as e:
            print(f"Erro ao importar arquivo: {str(e)}")
            return False
    
    def get_matrix(self, name: Optional[str] = None) -> Optional[pd.DataFrame]:
        """
        Retorna a matriz LCI especificada ou a atual.
        
        Args:
            name: Nome da matriz desejada
            
        Returns:
            DataFrame com os dados LCI
        """
        if name:
            return self._data.get(name)
        return self._current_matrix
    
    def list_available_matrices(self) -> List[str]:
        """
        Lista todas as matrizes LCI disponíveis.
        
        Returns:
            Lista com os nomes das matrizes
        """
        return list(self._data.keys())
    
    def validate_matrix(self, matrix: pd.DataFrame) -> bool:
        """
        Valida se a matriz LCI está no formato correto.
        
        Args:
            matrix: DataFrame com os dados LCI
            
        Returns:
            bool: True se a matriz é válida
        """
        try:
            # Verifica se há dados
            if matrix.empty:
                return False
            
            # Verifica se há valores negativos
            if (matrix.select_dtypes(include=[np.number]) < 0).any().any():
                return False
            
            # Verifica se há valores nulos
            if matrix.isnull().any().any():
                return False
            
            # Verifica se há pelo menos uma coluna de processo
            if 'Processo' not in matrix.columns:
                return False
            
            return True
        except Exception:
            return False
    
    def export_matrix(self, name: str, file_path: str) -> bool:
        """
        Exporta uma matriz LCI para arquivo.
        
        Args:
            name: Nome da matriz a ser exportada
            file_path: Caminho do arquivo de saída
            
        Returns:
            bool: True se a exportação foi bem-sucedida
        """
        try:
            matrix = self._data.get(name)
            if matrix is None:
                return False
            
            if file_path.endswith('.csv'):
                matrix.to_csv(file_path, index=False)
            elif file_path.endswith(('.xlsx', '.xls')):
                matrix.to_excel(file_path, index=False)
            else:
                raise ValueError("Formato de arquivo não suportado")
            
            return True
        except Exception as e:
            print(f"Erro ao exportar arquivo: {str(e)}")
            return False
    
    def get_matrix_metadata(self, name: str) -> Optional[Dict]:
        """
        Retorna os metadados de uma matriz LCI.
        
        Args:
            name: Nome da matriz
            
        Returns:
            Dicionário com os metadados
        """
        return self._metadata.get(name)
    
    def get_matrix_summary(self, name: Optional[str] = None) -> Dict:
        """
        Retorna um resumo estatístico da matriz LCI.
        
        Args:
            name: Nome da matriz (opcional)
            
        Returns:
            Dicionário com estatísticas
        """
        matrix = self.get_matrix(name)
        if matrix is None:
            return {}
        
        numeric_cols = matrix.select_dtypes(include=[np.number]).columns
        summary = {
            'total_rows': len(matrix),
            'total_columns': len(matrix.columns),
            'numeric_columns': len(numeric_cols),
            'column_stats': {}
        }
        
        for col in numeric_cols:
            summary['column_stats'][col] = {
                'mean': matrix[col].mean(),
                'std': matrix[col].std(),
                'min': matrix[col].min(),
                'max': matrix[col].max()
            }
        
        return summary 