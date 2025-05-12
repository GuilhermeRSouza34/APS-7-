"""
Testes unitários para o calculador de emergia.
"""
import pytest
import pandas as pd
import numpy as np
from ..core.emergy_calculator import EmergyCalculator

def test_emergy_calculation():
    """Testa o cálculo básico de emergia."""
    # Cria uma matriz de teste
    data = {
        'Processo1': [1.0, 2.0, 3.0],
        'Processo2': [2.0, 3.0, 4.0]
    }
    matrix = pd.DataFrame(data)
    
    # Configura fatores de transformidade
    calculator = EmergyCalculator()
    transformity_factors = {
        'Processo1': 2.0,
        'Processo2': 3.0
    }
    calculator.set_transformity_factors(transformity_factors)
    
    # Realiza o cálculo
    results = calculator.calculate_emergy(matrix)
    
    # Verifica os resultados
    expected = np.array([8.0, 13.0, 18.0])  # (1*2 + 2*3), (2*2 + 3*3), (3*2 + 4*3)
    np.testing.assert_array_almost_equal(results, expected)

def test_network_emergy_calculation():
    """Testa o cálculo de emergia em rede."""
    # Cria matrizes de teste
    input_data = {
        'Entrada1': [1.0, 2.0],
        'Entrada2': [2.0, 3.0]
    }
    process_data = {
        'Processo1': [3.0, 4.0],
        'Processo2': [4.0, 5.0]
    }
    
    input_matrix = pd.DataFrame(input_data)
    process_matrix = pd.DataFrame(process_data)
    
    # Configura calculadora
    calculator = EmergyCalculator()
    transformity_factors = {
        'Entrada1': 2.0,
        'Entrada2': 3.0,
        'Processo1': 4.0,
        'Processo2': 5.0
    }
    calculator.set_transformity_factors(transformity_factors)
    
    # Realiza o cálculo
    input_emergy, process_emergy = calculator.calculate_network_emergy(
        input_matrix, process_matrix
    )
    
    # Verifica os resultados
    expected_input = np.array([8.0, 13.0])  # (1*2 + 2*3), (2*2 + 3*3)
    expected_process = np.array([32.0, 41.0])  # (3*4 + 4*5), (4*4 + 5*5)
    
    np.testing.assert_array_almost_equal(input_emergy, expected_input)
    np.testing.assert_array_almost_equal(process_emergy, expected_process) 